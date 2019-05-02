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
	 "cordctl/format"
	 "github.com/fullstorydev/grpcurl"
	 flags "github.com/jessevdk/go-flags"
	 "github.com/jhump/protoreflect/dynamic"
//   "strings"
 )
 
 const (
	 DEFAULT_MODEL_FORMAT = "table{{ .Id }}\t{{ .Name }}"
 )
 
 type ModelList struct {
	 OutputOptions
	 Args struct {
		ModelName  string
     } `positional-args:"yes" required:"yes"`
 }
 
 type ModelListOutput struct {
	 Id          string
	 Name        string
 }
 
 type ModelOpts struct {
	 List    ModelList    `command:"list"`
 }
 
 var modelOpts = ModelOpts{}
 
 func RegisterModelCommands(parser *flags.Parser) {
	 parser.AddCommand("model", "model commands", "Commands to query and manipulate XOS models", &modelOpts)
 }

 func (options *ModelList) Execute(args []string) error {
 
	 conn, err := NewConnection()
	 if err != nil {
		 return err
	 }
	 defer conn.Close()

	 // TODO: Validate ModelName

	 method_name := "xos.xos/List" + options.Args.ModelName
 
	 descriptor, method, err := GetReflectionMethod(conn, method_name)
	 if err != nil {
		 return err
	 }
 
	 ctx, cancel := context.WithTimeout(context.Background(), GlobalConfig.Grpc.Timeout)
	 defer cancel()

	 headers := GenerateHeaders()
 
	 h := &RpcEventHandler{}
	 err = grpcurl.InvokeRPC(ctx, descriptor, conn, method, headers, h, h.GetParams)
	 if err != nil {
		 return err
	 }
 
	 if h.Status != nil && h.Status.Err() != nil {
		 return h.Status.Err()
	 }
 
	 d, err := dynamic.AsDynamicMessage(h.Response)
	 if err != nil {
		 return err
	 }
 
	 items, err := d.TryGetFieldByName("items")
	 if err != nil {
		 return err
	 }
 
	 outputFormat := CharReplacer.Replace(options.Format)
	 if outputFormat == "" {
		 outputFormat = DEFAULT_MODEL_FORMAT
	 }
	 if options.Quiet {
		 outputFormat = "{{.Id}}"
	 }
 
	 data := make([]ModelListOutput, len(items.([]interface{})))

	 // TODO: This whole thing needs to be made dynamic. We need to learn the fields in
	 // the message from the descriptor, put the fields into a table with all field names
	 // listed, etc.
 
	 for i, item := range items.([]interface{}) {
		 val := item.(*dynamic.Message)
		 data[i].Id = fmt.Sprint(val.GetFieldByName("id").(int32))
		 if val.HasFieldName("name") {
			data[i].Name = val.GetFieldByName("name").(string)
		 }
			 
	 }
 
	 result := CommandResult{
		 Format:   format.Format(outputFormat),
		 OutputAs: toOutputType(options.OutputAs),
		 Data:     data,
	 }
 
	 GenerateOutput(&result)
	 return nil
 }
 