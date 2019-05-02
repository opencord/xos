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
	 "cordctl/format"
	 "github.com/fullstorydev/grpcurl"
	 flags "github.com/jessevdk/go-flags"
	 "github.com/jhump/protoreflect/dynamic"
//   "strings"
 )
 
 const (
	 DEFAULT_SERVICE_FORMAT = "table{{ .Name }}\t{{.Version}}\t{{.State}}"
 )
 
 type ServiceList struct {
	 OutputOptions
 }
 
 type ServiceListOutput struct {
	 Name          string
	 Version       string
	 State         string
 }
 
 type ServiceOpts struct {
	 List    ServiceList    `command:"list"`
 }
 
 var serviceOpts = ServiceOpts{}
 
 func RegisterServiceCommands(parser *flags.Parser) {
	 parser.AddCommand("service", "service commands", "Commands to query and manipulate dynamically loaded XOS Services", &serviceOpts)
 }

 func (options *ServiceList) Execute(args []string) error {
 
	 conn, err := NewConnection()
	 if err != nil {
		 return err
	 }
	 defer conn.Close()
 
	 descriptor, method, err := GetReflectionMethod(conn, "xos.dynamicload.GetLoadStatus")
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
 
	 items, err := d.TryGetFieldByName("services")
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
 
	 data := make([]ServiceListOutput, len(items.([]interface{})))
 
	 for i, item := range items.([]interface{}) {
		 val := item.(*dynamic.Message)
		 data[i].Name = val.GetFieldByName("name").(string)
		 data[i].Version = val.GetFieldByName("version").(string)
		 data[i].State = val.GetFieldByName("state").(string)
	 }
 
	 result := CommandResult{
		 Format:   format.Format(outputFormat),
		 OutputAs: toOutputType(options.OutputAs),
		 Data:     data,
	 }
 
	 GenerateOutput(&result)
	 return nil
 }
 