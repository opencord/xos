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
	"encoding/json"
	"fmt"
	"cordctl/format"
	"google.golang.org/grpc"
	"gopkg.in/yaml.v2"
	"io/ioutil"
	"log"
	"os"
	"strings"
	"time"
)

type OutputType uint8

const (
	OUTPUT_TABLE OutputType = iota
	OUTPUT_JSON
	OUTPUT_YAML
)

var CharReplacer = strings.NewReplacer("\\t", "\t", "\\n", "\n")

type GrpcConfigSpec struct {
	Timeout time.Duration `yaml:"timeout"`
}

type TlsConfigSpec struct {
	UseTls bool   `yaml:"useTls"`
	CACert string `yaml:"caCert"`
	Cert   string `yaml:"cert"`
	Key    string `yaml:"key"`
	Verify string `yaml:"verify"`
}

type GlobalConfigSpec struct {
	ApiVersion string        `yaml:"apiVersion"`
	Server     string        `yaml:"server"`
	Username   string        `yaml:"username"`
	Password   string        `yaml:"password"`
	Tls        TlsConfigSpec `yaml:"tls"`
	Grpc       GrpcConfigSpec
}

var GlobalConfig = GlobalConfigSpec{
	ApiVersion: "v1",
	Server:     "localhost",
	Tls: TlsConfigSpec{
		UseTls: false,
	},
	Grpc: GrpcConfigSpec{
		Timeout: time.Second * 10,
	},
}

var GlobalOptions struct {
	Config     string `short:"c" long:"config" env:"CORDCONFIG" value-name:"FILE" default:"" description:"Location of client config file"`
	Server     string `short:"s" long:"server" default:"" value-name:"SERVER:PORT" description:"IP/Host and port of XOS"`
	Username   string `short:"u" long:"username" value-name:"USERNAME" default:"" description:"Username to authenticate with XOS"`
	Password   string `short:"p" long:"password" value-name:"PASSWORD" default:"" description:"Password to authenticate with XOS"`
	ApiVersion string `short:"a" long:"apiversion" description:"API version" value-name:"VERSION" choice:"v1" choice:"v2"`
	Debug      bool   `short:"d" long:"debug" description:"Enable debug mode"`
	UseTLS     bool   `long:"tls" description:"Use TLS"`
	CACert     string `long:"tlscacert" value-name:"CA_CERT_FILE" description:"Trust certs signed only by this CA"`
	Cert       string `long:"tlscert" value-name:"CERT_FILE" description:"Path to TLS vertificate file"`
	Key        string `long:"tlskey" value-name:"KEY_FILE" description:"Path to TLS key file"`
	Verify     bool   `long:"tlsverify" description:"Use TLS and verify the remote"`
}

type OutputOptions struct {
	Format   string `long:"format" value-name:"FORMAT" default:"" description:"Format to use to output structured data"`
	Quiet    bool   `short:"q" long:"quiet" description:"Output only the IDs of the objects"`
	OutputAs string `short:"o" long:"outputas" default:"table" choice:"table" choice:"json" choice:"yaml" description:"Type of output to generate"`
}

func toOutputType(in string) OutputType {
	switch in {
	case "table":
		fallthrough
	default:
		return OUTPUT_TABLE
	case "json":
		return OUTPUT_JSON
	case "yaml":
		return OUTPUT_YAML
	}
}

type CommandResult struct {
	Format   format.Format
	OutputAs OutputType
	Data     interface{}
}

type config struct {
	ApiVersion string `yaml:"apiVersion"`
	Server     string `yaml:"server"`
}

func NewConnection() (*grpc.ClientConn, error) {
	if len(GlobalOptions.Config) == 0 {
		home, err := os.UserHomeDir()
		if err != nil {
			log.Printf("Unable to discover they users home directory: %s\n", err)
		}
		GlobalOptions.Config = fmt.Sprintf("%s/.cord/config", home)
	}

	info, err := os.Stat(GlobalOptions.Config)
	if err == nil && !info.IsDir() {
		configFile, err := ioutil.ReadFile(GlobalOptions.Config)
		if err != nil {
			log.Printf("configFile.Get err   #%v ", err)
		}
		err = yaml.Unmarshal(configFile, &GlobalConfig)
		if err != nil {
			log.Fatalf("Unmarshal: %v", err)
		}
	}

	// Override from command line
	if GlobalOptions.Server != "" {
		GlobalConfig.Server = GlobalOptions.Server
	}
	if GlobalOptions.ApiVersion != "" {
		GlobalConfig.ApiVersion = GlobalOptions.ApiVersion
	}
	if GlobalOptions.Username != "" {
		GlobalConfig.Username = GlobalOptions.Username
	}
	if GlobalOptions.Password != "" {
		GlobalConfig.Password = GlobalOptions.Password
	}

	return grpc.Dial(GlobalConfig.Server, grpc.WithInsecure())
}

func GenerateOutput(result *CommandResult) {
	if result != nil && result.Data != nil {
		if result.OutputAs == OUTPUT_TABLE {
			tableFormat := format.Format(result.Format)
			tableFormat.Execute(os.Stdout, true, result.Data)
		} else if result.OutputAs == OUTPUT_JSON {
			asJson, err := json.Marshal(&result.Data)
			if err != nil {
				panic(err)
			}
			fmt.Printf("%s", asJson)
		} else if result.OutputAs == OUTPUT_YAML {
			asYaml, err := yaml.Marshal(&result.Data)
			if err != nil {
				panic(err)
			}
			fmt.Printf("%s", asYaml)
		}
	}
}
