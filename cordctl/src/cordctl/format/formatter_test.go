package format

import (
	"fmt"
	"strings"
	"testing"
)

type TestSubStructure struct {
	Value string
}

type TestStructure struct {
	Field1 string
	Field2 *string
	Field3 bool
	Field4 int
	Field5 []string
	Field6 [][]string
	Field7 TestSubStructure
	Field8 []TestSubStructure
	Field9 *TestSubStructure
}

func generateTestData(rows int) []TestStructure {
	data := make([]TestStructure, rows)

	abc := "abc"
	for i := 0; i < rows; i += 1 {
		data[i].Field1 = fmt.Sprintf("0x%05x", i)
		data[i].Field2 = &abc
		if i%2 == 0 {
			data[i].Field3 = true
		}
		data[i].Field4 = i
		data[i].Field5 = []string{"a", "b", "c", "d"}
		data[i].Field6 = [][]string{{"x", "y", "z"}}
		data[i].Field7.Value = "abc"
		data[i].Field8 = []TestSubStructure{{Value: "abc"}}
		data[i].Field9 = &TestSubStructure{Value: "abc"}
	}
	return data
}

func TestTableFormat(t *testing.T) {
	expected := "" +
		"FIELD1     FIELD2    FIELD3    FIELD4    FIELD5       FIELD6       VALUE    FIELD8     FIELD9\n" +
		"0x00000    abc       true      0         [a b c d]    [[x y z]]    abc      [{abc}]    {abc}\n" +
		"0x00001    abc       false     1         [a b c d]    [[x y z]]    abc      [{abc}]    {abc}\n" +
		"0x00002    abc       true      2         [a b c d]    [[x y z]]    abc      [{abc}]    {abc}\n" +
		"0x00003    abc       false     3         [a b c d]    [[x y z]]    abc      [{abc}]    {abc}\n" +
		"0x00004    abc       true      4         [a b c d]    [[x y z]]    abc      [{abc}]    {abc}\n" +
		"0x00005    abc       false     5         [a b c d]    [[x y z]]    abc      [{abc}]    {abc}\n" +
		"0x00006    abc       true      6         [a b c d]    [[x y z]]    abc      [{abc}]    {abc}\n" +
		"0x00007    abc       false     7         [a b c d]    [[x y z]]    abc      [{abc}]    {abc}\n" +
		"0x00008    abc       true      8         [a b c d]    [[x y z]]    abc      [{abc}]    {abc}\n" +
		"0x00009    abc       false     9         [a b c d]    [[x y z]]    abc      [{abc}]    {abc}\n"
	got := &strings.Builder{}
	format := Format("table{{.Field1}}\t{{.Field2}}\t{{.Field3}}\t{{.Field4}}\t{{.Field5}}\t{{.Field6}}\t{{.Field7.Value}}\t{{.Field8}}\t{{.Field9}}")
	data := generateTestData(10)
	err := format.Execute(got, true, data)
	if err != nil {
		t.Errorf("%s: unexpected error result: %s", t.Name(), err)
	}
	if got.String() != expected {
		t.Logf("RECEIVED:\n%s\n", got.String())
		t.Logf("EXPECTED:\n%s\n", expected)
		t.Errorf("%s: expected and received did not match", t.Name())
	}
}

func TestNoTableFormat(t *testing.T) {
	expected := "" +
		"0x00000,abc,true,0,[a b c d],[[x y z]],abc,[{abc}],{abc}\n" +
		"0x00001,abc,false,1,[a b c d],[[x y z]],abc,[{abc}],{abc}\n" +
		"0x00002,abc,true,2,[a b c d],[[x y z]],abc,[{abc}],{abc}\n" +
		"0x00003,abc,false,3,[a b c d],[[x y z]],abc,[{abc}],{abc}\n" +
		"0x00004,abc,true,4,[a b c d],[[x y z]],abc,[{abc}],{abc}\n" +
		"0x00005,abc,false,5,[a b c d],[[x y z]],abc,[{abc}],{abc}\n" +
		"0x00006,abc,true,6,[a b c d],[[x y z]],abc,[{abc}],{abc}\n" +
		"0x00007,abc,false,7,[a b c d],[[x y z]],abc,[{abc}],{abc}\n" +
		"0x00008,abc,true,8,[a b c d],[[x y z]],abc,[{abc}],{abc}\n" +
		"0x00009,abc,false,9,[a b c d],[[x y z]],abc,[{abc}],{abc}\n"
	got := &strings.Builder{}
	format := Format("{{.Field1}},{{.Field2}},{{.Field3}},{{.Field4}},{{.Field5}},{{.Field6}},{{.Field7.Value}},{{.Field8}},{{.Field9}}")
	data := generateTestData(10)
	err := format.Execute(got, false, data)
	if err != nil {
		t.Errorf("%s: unexpected error result: %s", t.Name(), err)
	}
	if got.String() != expected {
		t.Logf("RECEIVED:\n%s\n", got.String())
		t.Logf("EXPECTED:\n%s\n", expected)
		t.Errorf("%s: expected and received did not match", t.Name())
	}
}

func TestTableSingleFormat(t *testing.T) {
	expected := "" +
		"FIELD1     FIELD2    FIELD3    FIELD4    FIELD5       FIELD6       VALUE    FIELD8     FIELD9\n" +
		"0x00000    abc       true      0         [a b c d]    [[x y z]]    abc      [{abc}]    {abc}\n"
	got := &strings.Builder{}
	format := Format("table{{.Field1}}\t{{.Field2}}\t{{.Field3}}\t{{.Field4}}\t{{.Field5}}\t{{.Field6}}\t{{.Field7.Value}}\t{{.Field8}}\t{{.Field9}}")
	data := generateTestData(1)
	err := format.Execute(got, true, data[0])
	if err != nil {
		t.Errorf("%s: unexpected error result: %s", t.Name(), err)
	}
	if got.String() != expected {
		t.Logf("RECEIVED:\n%s\n", got.String())
		t.Logf("EXPECTED:\n%s\n", expected)
		t.Errorf("%s: expected and received did not match", t.Name())
	}
}

func TestNoTableSingleFormat(t *testing.T) {
	expected := "0x00000,abc,true,0,[a b c d],[[x y z]],abc,[{abc}],{abc}\n"
	got := &strings.Builder{}
	format := Format("{{.Field1}},{{.Field2}},{{.Field3}},{{.Field4}},{{.Field5}},{{.Field6}},{{.Field7.Value}},{{.Field8}},{{.Field9}}")
	data := generateTestData(1)
	err := format.Execute(got, false, data[0])
	if err != nil {
		t.Errorf("%s: unexpected error result: %s", t.Name(), err)
	}
	if got.String() != expected {
		t.Logf("RECEIVED:\n%s\n", got.String())
		t.Logf("EXPECTED:\n%s\n", expected)
		t.Errorf("%s: expected and received did not match", t.Name())
	}
}

func TestBadFormat(t *testing.T) {
	format := Format("table{{.Field1}\t{{.Field2}}\t{{.Field3}}\t{{.Field4}}\t{{.Field5}}\t{{.Field6}}\t{{.Field7.Value}}\t{{.Field8}}\t{{.Field9}}")
	got := &strings.Builder{}
	data := generateTestData(10)
	err := format.Execute(got, true, data)
	if err == nil {
		t.Errorf("%s: expected error (bad format) got none", t.Name())
	}
}
