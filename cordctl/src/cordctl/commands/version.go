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
	"cordctl/format"
	flags "github.com/jessevdk/go-flags"
)

type VersionOutput struct {
	Client  string `json:"client"`
}

type VersionOpts struct {
	OutputAs string `short:"o" long:"outputas" default:"table" choice:"table" choice:"json" choice:"yaml" description:"Type of output to generate"`
}

var versionOpts = VersionOpts{}

func RegisterVersionCommands(parent *flags.Parser) {
	parent.AddCommand("version", "display version", "Display client version", &versionOpts)
}

func (options *VersionOpts) Execute(args []string) error {
	result := CommandResult{
		Format:   format.Format("Client Version: {{.Client}}\n"),
		OutputAs: toOutputType(options.OutputAs),
		Data:     VersionOutput{Client: "beta"},
	}

	GenerateOutput(&result)
	return nil
}
