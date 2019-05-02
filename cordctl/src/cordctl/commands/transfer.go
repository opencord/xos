/*
 * Copyright 2019-present Ciena Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
 package commands

 import (
	 "context"
	 "fmt"
	 "io"
	 "cordctl/format"
	 "github.com/fullstorydev/grpcurl"
	 flags "github.com/jessevdk/go-flags"
	 "os"
	 "github.com/jhump/protoreflect/dynamic"
	 "github.com/golang/protobuf/proto"
//   "strings"
 )

 const (
	DEFAULT_UPLOAD_FORMAT = "table{{ .Status }}\t{{ .Checksum }}\t{{ .ChunksReceived }}\t{{ .BytesReceived }}"
 )
 
 type TransferUploadOutput struct {
	Status			  string
	Checksum          string
	ChunksReceived	  int32
	BytesReceived     int32
}
 
 type TransferUpload struct {
	 OutputOptions
	 Args struct {
		LocalFileName  string
		URI string
     } `positional-args:"yes" required:"yes"`
 }

 type TransferDownload struct {
	OutputOptions
	Args struct {
	   URI string
	   LocalFileName  string
	} `positional-args:"yes" required:"yes"`
}
 
 type TransferOpts struct {
	 Upload    TransferUpload    `command:"upload"`
	 Download  TransferDownload  `command:"download"`
 }
 
 var transferOpts = TransferOpts{}
 
 func RegisterTransferCommands(parser *flags.Parser) {
	 parser.AddCommand("transfer", "file transfer commands", "Commands to transfer files to and from XOS", &transferOpts)
 }

 func mkstreamer(uri string, f *os.File) func(proto.Message) error {
	// Create a callback that will stream a file. (Upload)
	return func(msg proto.Message) error {
		dmsg, err := dynamic.AsDynamicMessage(msg)
		if err != nil {
			return err
		}

		fmt.Printf("streamder, MessageName: %s\n", dmsg.XXX_MessageName())

		block := make([]byte, 80) // 65536)
		bytes_read, err := f.Read(block)

		if (err == io.EOF) {
			f.Close()
			fmt.Print("EOF\n")
			return err
		}

		if (err != nil) {
			fmt.Print("ERROR!\n")
			return err
		}

		dmsg.TrySetFieldByName("uri", uri)
		dmsg.TrySetFieldByName("chunk", string(block[:bytes_read]))

		return nil
	}
 }

 func (options *TransferUpload) Execute(args []string) error {
 
	 conn, err := NewConnection()
	 if err != nil {
		 return err
	 }
	 defer conn.Close()

	 local_name := options.Args.LocalFileName
	 uri := options.Args.URI
 
	 descriptor, method, err := GetReflectionMethod(conn, "xos.filetransfer/Upload")
	 if err != nil {
		 return err
	 }
 
	 ctx, cancel := context.WithTimeout(context.Background(), GlobalConfig.Grpc.Timeout)
	 defer cancel()

	 headers := GenerateHeaders()

	 f, err := os.Open(local_name)
	 if err != nil {
		return err
	 }
	 
	 h := &RpcEventHandler{}

	streamer := mkstreamer(uri, f)

	 err = grpcurl.InvokeRPC(ctx, descriptor, conn, method, headers, h, streamer)
	 if err != nil {
		 return err
	 }
	 d, err := dynamic.AsDynamicMessage(h.Response)
	 if err != nil {
		 return err
	 }

	 outputFormat := CharReplacer.Replace(options.Format)
	 if outputFormat == "" {
		 outputFormat = DEFAULT_UPLOAD_FORMAT
	 }
	 if options.Quiet {
		 outputFormat = "{{.Id}}"
	 }

	data := make([]TransferUploadOutput, 1)
	data[0].Checksum = d.GetFieldByName("checksum").(string)
    data[0].ChunksReceived = d.GetFieldByName("chunks_received").(int32)
	data[0].BytesReceived = d.GetFieldByName("bytes_received").(int32)

	// For constants, see filetransfer.proto FileUploadStatusCode enum
	switch d.GetFieldByName("status").(int32) {
		case 0:
			data[0].Status = "SUCCESS"
		case 1:
			data[0].Status = "ERROR"
		default:
			data[0].Status = "UNKNOWN"
	}

	result := CommandResult{
		Format:   format.Format(outputFormat),
		OutputAs: toOutputType(options.OutputAs),
		Data:     data,
	}

	GenerateOutput(&result)
		 

	 return nil
 }
 