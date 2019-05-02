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
//	 "fmt"
     "io"
	 "cordctl/format"
	 "github.com/fullstorydev/grpcurl"
	 flags "github.com/jessevdk/go-flags"
	 "os"
	 "github.com/jhump/protoreflect/dynamic"
//   "strings"
 )

 const (
	DEFAULT_UPLOAD_FORMAT = "table{{ .Checksum }}"
 )
 
 type TransferUploadOutput struct {
	Checksum          string
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
	 
	 for {
		 block := make([]byte, 65536)
		 bytes_read, err := f.Read(block)
		 if err == io.EOF {
			 break
		 }
		 if err != nil {
			 return err
		 }
		 if bytes_read <= 0 {
			 break
		 }

		 dm := make(map[string]interface{})
		 dm["uri"] = uri
		 dm["chunk"] = block

		 h := &RpcEventHandler{
			 Fields: map[string]map[string]interface{}{"xos.filetransfer.FileUploadChunk": dm},
		 }
		 err = grpcurl.InvokeRPC(ctx, descriptor, conn, method, headers, h, h.GetParams)
		 if err != nil {
			 return err
		 }
		 d, err := dynamic.AsDynamicMessage(h.Response)
		 if err != nil {
			 return err
		 }

		 outputFormat := CharReplacer.Replace(options.Format)
		 if outputFormat == "" {
			 outputFormat = DEFAULT_SERVICE_FORMAT
		 }
		 if options.Quiet {
			 outputFormat = "{{.Id}}"
		 }

		 data := make([]TransferUploadOutput, 1)
		 data[0].Checksum = d.GetFieldByName("checksum").(string)
//		 data[0].ChunksReceived = d.GetFieldByName("chunks_received").(int32)
//		 data[0].BytesReceived = d.GetFieldByName("bytes_received").(int32)

		 result := CommandResult{
			 Format:   format.Format(outputFormat),
			 OutputAs: toOutputType(options.OutputAs),
			 Data:     data,
		 }
	 
		 GenerateOutput(&result)
		 
	 }

	 return nil
 }
 