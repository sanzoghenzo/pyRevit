# import os.path
import clr
from collections import deque

from System.IO import StreamReader
from System.Reflection import MemberTypes
from System.Windows.Markup import XamlReader
clr.AddReference("System.Xaml")
from System.Xaml import XamlMember
from System.Xaml import XamlXmlReader
from System.Xaml import XamlObjectWriter
from System.Xaml import XamlObjectWriterSettings
from System.Xaml.Schema import XamlMemberInvoker


def LoadComponent(root, filename):
    # TODO: handle streams and strings as well
    reader = XamlXmlReader(StreamReader(filename), XamlReader.GetWpfSchemaContext())
    settings = XamlObjectWriterSettings()
    settings.RootObjectInstance = root
    writer = _DynamicWriter(root, reader.SchemaContext, settings)
    while reader.Read():
        writer.WriteNode(reader)
    for name in writer.names:
        value = writer.RootNameScope.FindName(name)
        if value is not None:
            setattr(root, name, value)
    return writer.Result


class _DynamicWriter(XamlObjectWriter):
    def __init__(self, scope, context, settings):
        super(_DynamicWriter, self).__init__(context, settings)
        self._scope = scope
        self._names = set()
        self._name_stack = deque()

    @property
    def names(self):
        return self._names

    def WriteValue(self, value):
        if self._name_stack[-1] and isinstance(value, str) and value:
            self._names.add(value)
        super(_DynamicWriter, self).WriteValue(value)

    def WriteEndMember(self):
        self._name_stack.pop()
        super(_DynamicWriter, self).WriteEndMember()

    def WriteStartMember(self, property):
        self._name_stack.append(
            property.Name == "Name" and property.Type.UnderlyingType == str
        )

        if property.UnderlyingMember and property.UnderlyingMember.MemberType == MemberTypes.Event:
            super(_DynamicWriter, self).WriteStartMember(
                _DynamicEventMember(self, property.UnderlyingMember, self.SchemaContext)
            )
        else:
            super(_DynamicWriter, self).WriteStartMember(property)


class _DynamicEventMember(XamlMember):
    def __init__(self, writer, event_info, context):
        super(_DynamicEventMember, self).__init__(
            event_info.Name,
            lambda: None,
            context,
            _DynamicEventInvoker(event_info, writer)
        )

class _DynamicEventInvoker(XamlMemberInvoker):
    def __init__(self, event_info, writer):
        super(_DynamicEventInvoker, self).__init__()
        self._writer = writer
        self._info = event_info

    def SetValue(self, instance, value):
        target = getattr(self._writer._scope, str(value))
        self._info.AddEventHandler(instance, target)
        # (Delegate)_writer._operations.ConvertTo(target, _info.EventHandlerType)
