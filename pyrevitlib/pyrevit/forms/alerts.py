import sys
from pyrevit import DB
from pyrevit import DOCS
from pyrevit import EXEC_PARAMS
from pyrevit import UI
from pyrevit import coreutils
from pyrevit import revit
from pyrevit import versionmgr
from pyrevit.coreutils.logger import get_logger

mlogger = get_logger(__name__)


def alert(
    msg,
    title=None,
    sub_msg=None,
    expanded=None,
    footer='',
    ok=True,
    cancel=False,
    yes=False,
    no=False,
    retry=False,
    warn_icon=True,
    options=None,
    exitscript=False
):
    r"""Show a task dialog with given message.

    Args:
        msg (str): message to be displayed
        title (str, optional): task dialog title
        sub_msg (str, optional): sub message, use html to create clickable links
        expanded (str, optional): expanded area message
        footer (str, optional): footer text
        ok (bool, optional): show OK button, defaults to True
        cancel (bool, optional): show Cancel button, defaults to False
        yes (bool, optional): show Yes button, defaults to False
        no (bool, optional): show NO button, defaults to False
        retry (bool, optional): show Retry button, defaults to False
        warn_icon (bool, optional): show warning icon
        options (list[str], optional): list of command link titles in order
        exitscript (bool, optional): exit if cancel or no, defaults to False

    Returns:
        (bool): True if okay, yes, or retry, otherwise False

    Examples:
        ```python
        from pyrevit import forms
        forms.alert(
            'Are you sure?',
            sub_msg='<a href="https://discourse.pyrevitlabs.io/">Click here if you are not sure and want to go to the pyRevit Forum</a>',
            ok=False,
            yes=True,
            no=True,
            exitscript=True
        )
        ```
    """
    # BUILD DIALOG
    cmd_name = EXEC_PARAMS.command_name
    if not title:
        title = cmd_name if cmd_name else 'pyRevit'
    tdlg = UI.TaskDialog(title)

    # process input types
    just_ok = ok and not any([cancel, yes, no, retry])

    options = options or []
    # add command links if any
    if options:
        clinks = coreutils.get_enum_values(UI.TaskDialogCommandLinkId)
        max_clinks = len(clinks)
        for idx, cmd in enumerate(options):
            if idx < max_clinks:
                tdlg.AddCommandLink(clinks[idx], cmd)
    # otherwise add buttons
    else:
        buttons = coreutils.get_enum_none(UI.TaskDialogCommonButtons)
        if yes:
            buttons |= UI.TaskDialogCommonButtons.Yes
        elif ok:
            buttons |= UI.TaskDialogCommonButtons.Ok

        if cancel:
            buttons |= UI.TaskDialogCommonButtons.Cancel
        if no:
            buttons |= UI.TaskDialogCommonButtons.No
        if retry:
            buttons |= UI.TaskDialogCommonButtons.Retry
        tdlg.CommonButtons = buttons

    # set texts
    tdlg.MainInstruction = msg
    tdlg.MainContent = sub_msg
    tdlg.ExpandedContent = expanded
    if footer:
        footer = footer.strip() + '\n'
    tdlg.FooterText = footer + 'pyRevit {}'.format(
        versionmgr.get_pyrevit_version().get_formatted()
        )
    tdlg.TitleAutoPrefix = False

    # set icon
    tdlg.MainIcon = \
        UI.TaskDialogIcon.TaskDialogIconWarning \
        if warn_icon else UI.TaskDialogIcon.TaskDialogIconNone

    # tdlg.VerificationText = 'verif'

    # SHOW DIALOG
    res = tdlg.Show()

    # PROCESS REPONSES
    # positive response
    mlogger.debug('alert result: %s', res)
    if res == UI.TaskDialogResult.Ok \
            or res == UI.TaskDialogResult.Yes \
            or res == UI.TaskDialogResult.Retry:
        if just_ok and exitscript:
            sys.exit()
        return True
    # negative response
    elif res == coreutils.get_enum_none(UI.TaskDialogResult) \
            or res == UI.TaskDialogResult.Cancel \
            or res == UI.TaskDialogResult.No:
        if exitscript:
            sys.exit()
        else:
            return False

    # command link response
    elif 'CommandLink' in str(res):
        tdresults = sorted(
            [x for x in coreutils.get_enum_values(UI.TaskDialogResult)
             if 'CommandLink' in str(x)]
            )
        residx = tdresults.index(res)
        return options[residx]
    elif exitscript:
        sys.exit()
    else:
        return False


def alert_ifnot(condition, msg, *args, **kwargs):
    """Show a task dialog with given message if condition is NOT met.

    Args:
        condition (bool): condition to test
        msg (str): message to be displayed
        *args (Any): additional arguments
        **kwargs (Any): additional keyword arguments

    Keyword Args:
        title (str, optional): task dialog title
        ok (bool, optional): show OK button, defaults to True
        cancel (bool, optional): show Cancel button, defaults to False
        yes (bool, optional): show Yes button, defaults to False
        no (bool, optional): show NO button, defaults to False
        retry (bool, optional): show Retry button, defaults to False
        exitscript (bool, optional): exit if cancel or no, defaults to False

    Returns:
        (bool): True if okay, yes, or retry, otherwise False

    Examples:
        ```python
        from pyrevit import forms
        forms.alert_ifnot(
            value > 12, 'Are you sure?', ok=False, yes=True, no=True, exitscript=True
        )
        ```
    """
    if not condition:
        return alert(msg, *args, **kwargs)


def inform_wip():
    """Show work-in-progress prompt to user and exit script.

    Examples:
        ```python
        forms.inform_wip()
        ```
    """
    alert("Work in progress.", exitscript=True)


def check_workshared(doc=None, message='Model is not workshared.'):
    """Verify if model is workshared and notify user if not.

    Args:
        doc (DB.Document): target document, current of not provided
        message (str): prompt message if returning False

    Returns:
        (bool): True if doc is workshared
    """
    doc = doc or DOCS.doc
    if doc.IsWorkshared:
        return True
    alert(message, warn_icon=True)
    return False


def check_selection(exitscript=False, message='At least one element must be selected.'):
    """Verify if selection is not empty notify user if it is.

    Args:
        exitscript (bool): exit script if returning False
        message (str): prompt message if returning False

    Returns:
        (bool): True if selection has at least one item
    """
    if not revit.get_selection().is_empty:
        return True
    alert(message, exitscript=exitscript)
    return False


def check_familydoc(doc=None, family_cat=None, exitscript=False):
    """Verify document is a Family and notify user if not.

    Args:
        doc (DB.Document): target document, current of not provided
        family_cat (str): family category name
        exitscript (bool): exit script if returning False

    Returns:
        (bool): True if doc is a Family and of provided category

    Examples:
        ```python
        from pyrevit import forms
        forms.check_familydoc(doc=revit.doc, family_cat='Data Devices')
        True
        ```
    """
    doc = doc or DOCS.doc
    family_cat = revit.query.get_category(family_cat)
    if (
        doc.IsFamilyDocument and
        (not family_cat or doc.OwnerFamily.FamilyCategory.Id == family_cat.Id)
    ):
        return True

    family_type_msg = ' of type {}'.format(family_cat.Name) if family_cat else''
    alert(
        'Active document must be a Family document{}.'.format(family_type_msg),
        exitscript=exitscript,
    )
    return False


def check_modeldoc(doc=None, exitscript=False):
    """Verify document is a not a Model and notify user if not.

    Args:
        doc (DB.Document): target document, current of not provided
        exitscript (bool): exit script if returning False

    Returns:
        (bool): True if doc is a Model

    Examples:
        ```python
        from pyrevit import forms
        forms.check_modeldoc(doc=revit.doc)
        True
        ```
    """
    doc = doc or DOCS.doc
    if not doc.IsFamilyDocument:
        return True
    alert(
        'Active document must be a Revit model (not a Family).', exitscript=exitscript
    )
    return False


def check_modelview(view, exitscript=False):
    """Verify target view is a model view.

    Args:
        view (DB.View): target view
        exitscript (bool): exit script if returning False

    Returns:
        (bool): True if view is model view

    Examples:
        ```python
        from pyrevit import forms
        forms.check_modelview(view=revit.active_view)
        True
        ```
    """
    if isinstance(view, (DB.View3D, DB.ViewPlan, DB.ViewSection)):
        return True    
    alert("Active view must be a model view.", exitscript=exitscript)
    return False


def check_viewtype(view, view_type, exitscript=False):
    """Verify target view is of given type.

    Args:
        view (DB.View): target view
        view_type (DB.ViewType): type of view
        exitscript (bool): exit script if returning False

    Returns:
        (bool): True if view is of given type

    Examples:
        ```python
        from pyrevit import forms
        forms.check_viewtype(revit.active_view, DB.ViewType.DrawingSheet)
        True
        ```
    """
    if view.ViewType == view_type:
        return True
    vt_string = ' '.join(coreutils.split_words(str(view_type)))
    alert("Active view must be a {}.".format(vt_string), exitscript=exitscript)
    return False


def check_graphicalview(view, exitscript=False):
    """Verify target view is a graphical view.

    Args:
        view (DB.View): target view
        exitscript (bool): exit script if returning False

    Returns:
        (bool): True if view is a graphical view

    Examples:
        ```python
        from pyrevit import forms
        forms.check_graphicalview(revit.active_view)
        True
        ```
    """
    if view.Category:
        return True
    alert("Active view must be a grahical view.", exitscript=exitscript)
    return False
