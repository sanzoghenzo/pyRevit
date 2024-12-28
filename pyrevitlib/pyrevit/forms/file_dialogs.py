from pyrevit import coreutils
from pyrevit.framework import CPDialogs
from pyrevit.framework import Forms


def pick_file(
    file_ext='*',
    files_filter='',
    init_dir='',
    restore_dir=True,
    multi_file=False,
    unc_paths=False,
    title=None
):
    r"""Pick file dialog to select a destination file.

    Args:
        file_ext (str): file extension
        files_filter (str): file filter
        init_dir (str): initial directory
        restore_dir (bool): restore last directory
        multi_file (bool): allow select multiple files
        unc_paths (bool): return unc paths
        title (str): text to show in the title bar

    Returns:
        (str | list[str]): file path or list of file paths if multi_file=True

    Examples:
        ```python
        from pyrevit import forms
        forms.pick_file(file_ext='csv')
        r'C:\output\somefile.csv'
        ```

        ```python
        forms.pick_file(file_ext='csv', multi_file=True)
        [r'C:\output\somefile1.csv', r'C:\output\somefile2.csv']
        ```

        ```python
        forms.pick_file(files_filter='All Files (*.*)|*.*|'
                                         'Excel Workbook (*.xlsx)|*.xlsx|'
                                         'Excel 97-2003 Workbook|*.xls',
                            multi_file=True)
        [r'C:\output\somefile1.xlsx', r'C:\output\somefile2.xls']
        ```
    """
    of_dlg = Forms.OpenFileDialog()
    if files_filter:
        of_dlg.Filter = files_filter
    else:
        of_dlg.Filter = '|*.{}'.format(file_ext)
    of_dlg.RestoreDirectory = restore_dir
    of_dlg.Multiselect = multi_file
    if init_dir:
        of_dlg.InitialDirectory = init_dir
    if title:
        of_dlg.Title = title
    if of_dlg.ShowDialog() == Forms.DialogResult.OK:
        if multi_file:
            if unc_paths:
                return [coreutils.dletter_to_unc(x)
                        for x in of_dlg.FileNames]
            return of_dlg.FileNames
        else:
            if unc_paths:
                return coreutils.dletter_to_unc(of_dlg.FileName)
            return of_dlg.FileName


def save_file(file_ext='', files_filter='', init_dir='', default_name='',
              restore_dir=True, unc_paths=False, title=None):
    r"""Save file dialog to select a destination file for data.

    Args:
        file_ext (str): file extension
        files_filter (str): file filter
        init_dir (str): initial directory
        default_name (str): default file name
        restore_dir (bool): restore last directory
        unc_paths (bool): return unc paths
        title (str): text to show in the title bar

    Returns:
        (str): file path

    Examples:
        ```python
        from pyrevit import forms
        forms.save_file(file_ext='csv')
        r'C:\output\somefile.csv'
        ```
    """
    sf_dlg = Forms.SaveFileDialog()
    if files_filter:
        sf_dlg.Filter = files_filter
    else:
        sf_dlg.Filter = '|*.{}'.format(file_ext)
    sf_dlg.RestoreDirectory = restore_dir
    if init_dir:
        sf_dlg.InitialDirectory = init_dir
    if title:
        sf_dlg.Title = title

    # setting default filename
    sf_dlg.FileName = default_name

    if sf_dlg.ShowDialog() == Forms.DialogResult.OK:
        if unc_paths:
            return coreutils.dletter_to_unc(sf_dlg.FileName)
        return sf_dlg.FileName


def pick_excel_file(save=False, title=None):
    """File pick/save dialog for an excel file.

    Args:
        save (bool): show file save dialog, instead of file pick dialog
        title (str): text to show in the title bar

    Returns:
        (str): file path
    """
    if save:
        return save_file(file_ext='xlsx')
    return pick_file(
        files_filter='Excel Workbook (*.xlsx)|*.xlsx|Excel 97-2003 Workbook|*.xls',
        title=title
    )


def save_excel_file(title=None):
    """File save dialog for an excel file.

    Args:
        title (str): text to show in the title bar

    Returns:
        (str): file path
    """
    return pick_excel_file(save=True, title=title)


def pick_folder(title=None, owner=None):
    """Show standard windows pick folder dialog.

    Args:
        title (str, optional): title for the window
        owner (object, optional): owner of the dialog

    Returns:
        (str): folder path
    """
    if CPDialogs:
        fb_dlg = CPDialogs.CommonOpenFileDialog()
        fb_dlg.IsFolderPicker = True
        if title:
            fb_dlg.Title = title

        res = CPDialogs.CommonFileDialogResult.Cancel
        if owner:
            res = fb_dlg.ShowDialog(owner)
        else:
            res = fb_dlg.ShowDialog()

        if res == CPDialogs.CommonFileDialogResult.Ok:
            return fb_dlg.FileName
    else:
        fb_dlg = Forms.FolderBrowserDialog()
        if title:
            fb_dlg.Description = title
        if fb_dlg.ShowDialog() == Forms.DialogResult.OK:
            return fb_dlg.SelectedPath
