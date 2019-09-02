package persistence

import (
	"fmt"

	"../cli"
	"github.com/asaskevich/govalidator"
)

// v1.0
type EngineInfoV1 struct {
	Version  string   `json:"version" bson:"version"`
	SysPaths []string `json:"syspath" bson:"syspath"`
}

type TraceInfoV1 struct {
	EngineInfo          EngineInfoV1 `json:"engine" bson:"engine"`
	IronPythonTraceDump string       `json:"ipy" bson:"ipy"`
	CLRTraceDump        string       `json:"clr" bson:"clr"`
}

type ScriptTelemetryRecordV1 struct {
	Date              string            `json:"date" bson:"date"`
	Time              string            `json:"time" bson:"time"`
	UserName          string            `json:"username" bson:"username"`
	RevitVersion      string            `json:"revit" bson:"revit"`
	RevitBuild        string            `json:"revitbuild" bson:"revitbuild"`
	SessionId         string            `json:"sessionid" bson:"sessionid"`
	PyRevitVersion    string            `json:"pyrevit" bson:"pyrevit"`
	IsDebugMode       bool              `json:"debug" bson:"debug"`
	IsConfigMode      bool              `json:"config" bson:"config"`
	CommandName       string            `json:"commandname" bson:"commandname"`
	CommandUniqueName string            `json:"commanduniquename" bson:"commanduniquename"`
	BundleName        string            `json:"commandbundle" bson:"commandbundle"`
	ExtensionName     string            `json:"commandextension" bson:"commandextension"`
	ResultCode        int               `json:"resultcode" bson:"resultcode"`
	CommandResults    map[string]string `json:"commandresults" bson:"commandresults"`
	ScriptPath        string            `json:"scriptpath" bson:"scriptpath"`
	TraceInfo         TraceInfoV1       `json:"trace" bson:"trace"`
}

func (logrec ScriptTelemetryRecordV1) PrintRecordInfo(logger *cli.Logger, message string) {
	logger.Print(fmt.Sprintf(
		"%s %s-%s %q @ %s:%s [%s.%s] code=%d info=%v",
		message,
		logrec.Date,
		logrec.Time,
		logrec.UserName,
		logrec.RevitBuild,
		logrec.TraceInfo.EngineInfo.Version,
		logrec.ExtensionName,
		logrec.CommandName,
		logrec.ResultCode,
		logrec.CommandResults,
	))
}

func (logrec ScriptTelemetryRecordV1) Validate() {
}

// v2.0
type EngineInfoV2 struct {
	Type     string                 `json:"type" bson:"type" valid:"-"`
	Version  string                 `json:"version" bson:"version" valid:"-"`
	SysPaths []string               `json:"syspath" bson:"syspath" valid:"-"`
	Configs  map[string]interface{} `json:"configs" bson:"configs" valid:"-"`
}

type TraceInfoV2 struct {
	EngineInfo EngineInfoV2 `json:"engine" bson:"engine" valid:"-"`
	Message    string       `json:"message" bson:"message" valid:"-"`
}

type RecordMetaV2 struct {
	SchemaVersion string `json:"schema" bson:"schema" valid:"-"`
}

type ScriptTelemetryRecordV2 struct {
	RecordMeta        RecordMetaV2           `json:"meta" bson:"meta" valid:"-"`                 // added in v2.0
	TimeStamp         string                 `json:"timestamp" bson:"timestamp" valid:"rfc3339"` // added in v2.0
	UserName          string                 `json:"username" bson:"username" valid:"-"`
	RevitVersion      string                 `json:"revit" bson:"revit" valid:"numeric"`
	RevitBuild        string                 `json:"revitbuild" bson:"revitbuild" valid:"matches(\\d{8}_\\d{4}\\(x\\d{2}\\))"`
	SessionId         string                 `json:"sessionid" bson:"sessionid" valid:"uuidv4"`
	PyRevitVersion    string                 `json:"pyrevit" bson:"pyrevit" valid:"-"`
	Clone             string                 `json:"clone" bson:"clone" valid:"-"` // added in v2.0
	IsDebugMode       bool                   `json:"debug" bson:"debug" valid:"-"`
	IsConfigMode      bool                   `json:"config" bson:"config" valid:"-"`
	IsExecFromGUI     bool                   `json:"from_gui" bson:"from_gui" valid:"-"` // added in v2.0
	CommandName       string                 `json:"commandname" bson:"commandname" valid:"-"`
	CommandUniqueName string                 `json:"commanduniquename" bson:"commanduniquename" valid:"-"`
	BundleName        string                 `json:"commandbundle" bson:"commandbundle" valid:"-"`
	ExtensionName     string                 `json:"commandextension" bson:"commandextension" valid:"-"`
	DocumentName      string                 `json:"docname" bson:"docname" valid:"-"` // added in v2.0
	DocumentPath      string                 `json:"docpath" bson:"docpath" valid:"-"` // added in v2.0
	ResultCode        int                    `json:"resultcode" bson:"resultcode" valid:"-"`
	CommandResults    map[string]interface{} `json:"commandresults" bson:"commandresults" valid:"-"`
	ScriptPath        string                 `json:"scriptpath" bson:"scriptpath" valid:"-"`
	TraceInfo         TraceInfoV2            `json:"trace" bson:"trace" valid:"-"` // revised in v2.0
}

func (logrec ScriptTelemetryRecordV2) PrintRecordInfo(logger *cli.Logger, message string) {
	logger.Print(fmt.Sprintf(
		"%s %s %q %s:%s (%s) [%s.%s] code=%d info=%v",
		message,
		logrec.TimeStamp,
		logrec.UserName,
		logrec.RevitBuild,
		logrec.TraceInfo.EngineInfo.Version,
		logrec.TraceInfo.EngineInfo.Type,
		logrec.ExtensionName,
		logrec.CommandName,
		logrec.ResultCode,
		logrec.CommandResults,
	))
}

func (logrec ScriptTelemetryRecordV2) Validate() error {
	govalidator.SetFieldsRequiredByDefault(true)
	_, err := govalidator.ValidateStruct(logrec)
	return err
}

// introduced with api v2
type EventTelemetryRecordV2 struct {
	RecordMeta   RecordMetaV2           `json:"meta" bson:"meta"`
	TimeStamp    string                 `json:"timestamp" bson:"timestamp"`
	EventType    string                 `json:"type" bson:"type"`
	EventArgs    map[string]interface{} `json:"args" bson:"args"`
	UserName     string                 `json:"username" bson:"username"`
	HostUserName string                 `json:"host_user" bson:"host_user"`
	RevitVersion string                 `json:"revit" bson:"revit"`
	RevitBuild   string                 `json:"revitbuild" bson:"revitbuild"`

	// general
	Cancellable      bool   `json:"cancellable" bson:"cancellable"`
	Cancelled        bool   `json:"cancelled" bson:"cancelled"`
	DocumentId       int    `json:"docid" bson:"docid"`
	DocumentType     string `json:"doctype" bson:"doctype"`
	DocumentTemplate string `json:"doctemplate" bson:"doctemplate"`
	DocumentName     string `json:"docname" bson:"docname"`
	DocumentPath     string `json:"docpath" bson:"docpath"`
	ProjectNumber    string `json:"projectnum" bson:"projectnum"`
	ProjectName      string `json:"projectname" bson:"projectname"`
}

func (logrec EventTelemetryRecordV2) PrintRecordInfo(logger *cli.Logger, message string) {
	if logrec.RecordMeta.SchemaVersion == "2.0" {
		logger.Print(fmt.Sprintf(
			"%s %s [%s] %q @ %s doc=%q @ %s",
			message,
			logrec.TimeStamp,
			logrec.EventType,
			logrec.HostUserName,
			logrec.RevitBuild,
			logrec.DocumentName,
			logrec.DocumentPath,
		))
	}
}

func (logrec EventTelemetryRecordV2) Validate() {
	// todo: validate by schema version
	if logrec.RecordMeta.SchemaVersion == "2.0" {
	}
}
