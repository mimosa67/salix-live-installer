#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Graphical Salix Live Installer configuration gathering.
"""
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'

import gettext
import gobject
import gtk
import gtk.glade
import re
import math
import subprocess
from datetime import *
from common import *
from config import *
from installer import *
import salix_livetools_library as sltl

class GatherGui:
  """
  GUI to gather information about the configuration to install.
  """
  def __init__(self, version, min_salt_version, is_test = False, is_test_clone = False, use_test_data = False):
    self.cfg = Config(min_salt_version, is_test, is_test_clone, use_test_data)
    builder = gtk.Builder()
    for d in ('./resources', '../resources'):
      if os.path.exists(d + '/salix-live-installer.glade'):
        builder.add_from_file(d + '/salix-live-installer.glade')
        break
    # Get a handle on the glade file widgets we want to interact with
    self.AboutDialog = builder.get_object("about_dialog")
    self.AboutDialog.set_version(version)
    self.Window = builder.get_object("main_window")
    self.ProgressWindow = builder.get_object("progress_dialog")
    self.InstallProgressBar = builder.get_object("install_progressbar")
    self.CancelProgressButton = builder.get_object("progress_undo")
    self.TimeTab = builder.get_object("time_tab")
    self.KeyboardTab = builder.get_object("keyboard_tab")
    self.LocaleTab = builder.get_object("locale_tab")
    self.PartitionTab = builder.get_object("partition_tab")
    self.UsersTab = builder.get_object("users_tab")
    self.PackagesTab = builder.get_object("packages_tab")
    self.BootloaderTab = builder.get_object("bootloader_tab")
    self.TimeCheck = builder.get_object("time_check")
    self.KeyboardCheck = builder.get_object("keyboard_check")
    self.LocaleCheck = builder.get_object("locale_check")
    self.PartitionCheck = builder.get_object("partition_check")
    self.UsersCheck = builder.get_object("users_check")
    self.PackagesCheck = builder.get_object("packages_check")
    self.BootloaderCheck = builder.get_object("bootloader_check")
    self.TimeCheckMarker = builder.get_object("time_check_marker")
    self.KeyboardCheckMarker = builder.get_object("keyboard_check_marker")
    self.LocaleCheckMarker = builder.get_object("locale_check_marker")
    self.PartitionCheckMarker = builder.get_object("partition_check_marker")
    self.UsersCheckMarker = builder.get_object("users_check_marker")
    self.PackagesCheckMarker = builder.get_object("packages_check_marker")
    self.BootloaderCheckMarker = builder.get_object("bootloader_check_marker")
    self.IntroBox = builder.get_object("intro_box")
    self.TimeBox = builder.get_object("time_box")
    self.KeyboardBox = builder.get_object("keyboard_box")
    self.LocaleBox = builder.get_object("locale_box")
    self.PartitioningBox = builder.get_object("partitioning_box")
    self.MainPartitionBox = builder.get_object("main_partition_box")
    self.LinuxPartitionBox = builder.get_object("linux_partition_box")
    self.WindowsPartitionBox = builder.get_object("windows_partition_box")
    self.RecapPartitionBox = builder.get_object("recap_partition_box")
    self.UsersBox = builder.get_object("users_box")
    self.PackagesBox = builder.get_object("packages_box")
    self.BootloaderBox = builder.get_object("bootloader_box")
    self.KeyboardList = builder.get_object("keyboard_list")
    self.KeyboardListStore = builder.get_object("keymap_list_store")
    self.KeyboardSelection = builder.get_object("keyboard_selection")
    self.LocaleList = builder.get_object("locale_list")
    self.LocaleListStore = builder.get_object("locale_list_store")
    self.LocaleSelection = builder.get_object("locale_selection")
    self.MainPartitionList = builder.get_object("main_partition_list")
    self.MainPartitionListStore = builder.get_object("main_partition_list_store")
    self.MainFormatCombobox = builder.get_object("main_format_combobox")
    self.MainFormatListStore = builder.get_object("main_format_list_store")
    self.LinuxPartitionList = builder.get_object("linux_partition_list")
    self.LinuxPartitionListStore = builder.get_object("linux_partition_list_store")
    self.WindowsPartitionList = builder.get_object("win_partition_list")
    self.WindowsPartitionListStore = builder.get_object("win_partition_list_store")
    self.RecapPartitionList = builder.get_object("recap_partition_list")
    self.RecapPartitionListStore = builder.get_object("recap_partition_list_store")
    self.YesNoDialog = builder.get_object("yes_no_dialog")
    self.LinuxNewSysComboCell = builder.get_object("linux_newsys_renderer_combo")
    self.LinuxNewSysColumn = builder.get_object("linux_newsys_column")
    self.LinuxFormatListStore = builder.get_object("linux_format_list_store")
    self.LinuxMountPointListStore = builder.get_object("linux_mountpoint_list_store")
    self.LinuxNewMountComboCell = builder.get_object("linux_newmount_renderer_combo")
    self.LinuxNewMountColumn = builder.get_object("linux_newmount_column")
    self.LinuxMountListStore = builder.get_object("linux_mountpoint_list_store")
    self.LinuxPartitionApply = builder.get_object("linux_partition_apply")
    self.WinMountPointListStore = builder.get_object("win_mountpoint_list_store")
    self.WindowsPartitionApply = builder.get_object("windows_partition_apply")
    self.WinMountComboCell = builder.get_object("win_newmount_renderer_combo")
    self.WinMountColumn = builder.get_object("win_newmount_column")
    self.WinMountListStore = builder.get_object("win_mountpoint_list_store")
    self.MainPartRecapLabel = builder.get_object("main_part_recap_label")
    self.LinPartRecapLabel = builder.get_object("lin_part_recap_label")
    self.WinPartRecapLabel = builder.get_object("win_part_recap_label")
    self.SwapPartRecapLabel = builder.get_object("swap_part_recap_label")
    self.CoreRadioButton = builder.get_object("core_radiobutton")
    self.CoreHBox = builder.get_object("core_hbox")
    self.BasicRadioButton = builder.get_object("basic_radiobutton")
    self.BasicHBox = builder.get_object("basic_hbox")
    self.FullRadioButton = builder.get_object("full_radiobutton")
    self.PackagesUndoButton = builder.get_object("packages_undo")
    self.PackagesApplyButton = builder.get_object("packages_apply")
    self.NobootloaderRadioButton = builder.get_object("nobootloader_radiobutton")
    self.LiloRadioButton = builder.get_object("lilo_radiobutton")
    self.Grub2RadioButton = builder.get_object("grub2_radiobutton")
    self.BootloaderUndoButton = builder.get_object("bootloader_undo")
    self.BootloaderApplyButton = builder.get_object("bootloader_apply")
    self.TimeUndoButton = builder.get_object("time_undo")
    self.TimeApplyButton = builder.get_object("time_apply")
    self.KeyboardUndoButton = builder.get_object("keyboard_undo")
    self.KeyboardApplyButton = builder.get_object("keyboard_apply")
    self.LocaleUndoButton = builder.get_object("locale_undo")
    self.LocaleApplyButton = builder.get_object("locale_apply")
    self.CloneLoginEventbox = builder.get_object("clone_login_eventbox")
    self.UsersEventbox = builder.get_object("users_eventbox")
    self.CloneLoginCheckbutton = builder.get_object("clone_login_checkbutton")
    self.CloneLoginUndo = builder.get_object("clone_login_undo")
    self.CloneLoginApply = builder.get_object("clone_login_apply")
    self.UserLoginEntry = builder.get_object("user_login_entry")
    self.UserPass1Entry = builder.get_object("user_pass1_entry")
    self.UserPass1Entry.set_visibility(False)
    self.UserPass2Entry = builder.get_object("user_pass2_entry")
    self.UserPass2Entry.set_visibility(False)
    self.UserPassStrength = builder.get_object("user_pass_strength")
    self.RootPass1Entry = builder.get_object("root_pass1_entry")
    self.RootPass1Entry.set_visibility(False)
    self.RootPass2Entry = builder.get_object("root_pass2_entry")
    self.RootPass2Entry.set_visibility(False)
    self.RootPassStrength = builder.get_object("root_pass_strength")
    self.UserVisibleCheckButton = builder.get_object("user_visible_checkbutton")
    self.RootVisibleCheckButton = builder.get_object("root_visible_checkbutton")
    self.ExternalDeviceCheckButton = builder.get_object("external_device_checkbutton")
    self.NumLockCheckButton = builder.get_object("numlock_checkbutton")
    self.IBusCheckButton = builder.get_object("ibus_checkbutton")
    self.RootPassCreated = builder.get_object("root_pass_created")
    self.NewUserLogin = builder.get_object("new_user_login")
    self.UsersUndoButton = builder.get_object("users_undo")
    self.UsersApplyButton = builder.get_object("users_apply")
    self.RootPassUndoButton = builder.get_object("rootpass_undo")
    self.RootPassApplyButton = builder.get_object("rootpass_apply")
    self.InstallButton = builder.get_object("install_button")
    self.YearCombobox = builder.get_object("year_combobox")
    self.MonthCombobox = builder.get_object("month_combobox")
    self.DayCombobox = builder.get_object("day_combobox")
    self.ContinentZoneCombobox = builder.get_object("continent_zone_combobox")
    self.CountryZoneCombobox = builder.get_object("country_zone_combobox")
    self.YearListStore = builder.get_object("year_list_store")
    self.MonthListStore = builder.get_object("month_list_store")
    self.DayListStore = builder.get_object("day_list_store")
    self.ContinentZoneListStore = builder.get_object("continent_zone_list_store")
    self.CountryZoneListStore = builder.get_object("country_zone_list_store")
    self.NTPCheckButton = builder.get_object("ntp_checkbutton")
    self.ManualTimeBox = builder.get_object("manual_time_box")
    self.HourSpinButton = builder.get_object("hour_spinbutton")
    self.MinuteSpinButton = builder.get_object("minute_spinbutton")
    self.SecondSpinButton = builder.get_object("second_spinbutton")
    self.TimeZoneBox = builder.get_object("time_zone_box")
    self.ContextLabel = builder.get_object("context_label")
    self.LayoutColumn = builder.get_object("layout_column")
    self.TypeColumn = builder.get_object("type_column")
    self.LocaleColumn = builder.get_object("locale_column")
    self.DescriptColumn = builder.get_object("descript_column")
    self.MainDiskColumn = builder.get_object("main_disk_column")
    self.MainPartColumn = builder.get_object("main_part_column")
    self.MainSizeColumn = builder.get_object("main_size_column")
    self.MainFormatColumn = builder.get_object("main_format_column")
    self.LinuxPartColumn = builder.get_object("linux_part_column")
    self.LinuxSizeColumn = builder.get_object("linux_size_column")
    self.LinuxOldSysColumn = builder.get_object("linux_oldsys_column")
    self.LinuxNewSysColumn = builder.get_object("linux_newsys_column")
    self.LinuxNewMountColumn = builder.get_object("linux_newmount_column")
    self.WinPartColumn = builder.get_object("win_part_column")
    self.WinSizeColumn = builder.get_object("win_size_column")
    self.WinOldSysColumn = builder.get_object("win_oldsys_column")
    self.WinNewMountColumn = builder.get_object("win_newmount_column")
    # Initialize the contextual help box
    self.context_intro = _("Contextual help.")
    self.on_leave_notify_event(None)
    self.build_data_stores()
    if self.cfg.use_test_data:
      self.time_settings()
      self.keyboard_settings()
      self.locale_settings()
      self.partitions_settings()
      self.users_settings()
      self.packages_settings()
      self.bootloader_settings()
      self.on_bootloader_tab_clicked(None)
    self.update_install_button()
    # Connect signals
    self.add_custom_signals()
    builder.connect_signals(self)

  # General contextual help
  def on_leave_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(self.context_intro)
  def on_intro_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("General usage."))
  def on_about_link_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("About Salix Installer."))
  def on_context_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Contextual help."))
  def on_button_quit_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Exit Salix Installer."))
  def on_install_button_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Launch Salix installation. This button will not be active until \
all settings are configured correctly."))
  def on_launch_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Launch Salix installation. This button will not be active until \
all settings are configured correctly."))

  # Time contextual help
  def on_time_tab_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Access the time settings."))
  def on_ntp_checkbutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Use Network Time Protocol daemon to synchronize time via Internet."))
  def on_time_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel time settings."))
  def on_time_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Activate the time settings after options have been defined."))
  def on_manual_time_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Set the date & time manually if you do not use NTP service."))
  def on_timezone_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Set the time zone."))

  # Keyboard contextual help
  def on_keyboard_tab_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Access the keyboard settings."))
  def on_keyboard_list_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Highlight your favorite keyboard layout \
from this list before clicking on the 'Select keyboard' button."))
  def on_numlock_checkbutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Check this box if you want your numeric keypad \
to be activated during the boot process."))
  def on_ibus_checkbutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Check this box if you want iBus to be \
activated during the boot process. IBus is an input method (IM) framework for multilingual input."))
  def on_keyboard_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel keyboard layout selection."))
  def on_keyboard_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Confirm your selection after highlighting the keyboard layout."))
  def on_keyboard_selection_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("This is the keyboard layout you have selected. \
'None' will be displayed until you have confirmed that selection."))

  # Locale contextual help
  def on_locale_tab_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Access the language settings."))
  def on_locale_list_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Highlight your language from this list before \
clicking on the 'Select language' button."))
  def on_locale_selection_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("This is the system language you have selected. \
'None' will be displayed until you have confirmed that selection."))
  def on_locale_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel language selection."))
  def on_locale_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Confirm your selection after highlighting the system language."))

  # Partitions contextual help
  def on_partition_tab_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Access the partitions settings."))
  def on_main_partition_list_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Highlight the partition from this list before \
clicking on the 'Select partition' button."))
  def on_external_device_checkbutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Check this box if you want your external disk drives \
to be displayed in the list above."))
  def on_main_partition_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Confirm your selection after highlighting the partition."))
  def on_main_format_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("The filesystem that will be used to format Salix main partition."))
  def on_linux_partition_list_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Click on the appropriate 'Select...' cell if you wish to modify the \
filesystem of a partition and/or if you wish to assign its mount point.\
You can either choose one of the suggested mount points or enter \
your own. You must configure all the desired partitions before clicking \
on the 'Apply settings' button. Any unset parameters will be ignored."))
  def on_linux_partition_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Confirm the Linux partitions settings from the list."))
  def on_win_partition_list_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Click on the appropriate 'Select...' cell if you wish to assign \
the mount point of a partition. You must configure all the \
desired partitions before clicking on the 'Apply settings' button. \
Any unset parameters will be ignored."))
  def on_windows_partition_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Confirm the Windows partitions settings from the list above."))
  def on_partition_recap_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Summary of your partitions settings."))
  def on_partition_recap_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel all partitions settings."))

  # Users contextual help
  def on_users_tab_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Access the users and passwords settings."))
  def on_clone_login_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Salix Live Installer has detected a \
LiveClone customized environment. You can transfer your existing LiveClone \
login accounts along with matching personal directories to the installation \
target or you can wipe them out and create a complete new login account instead."))
  def on_clone_login_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Transfer existing users."))
  def on_clone_login_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel users transfer."))
  def on_users_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("A Linux system can manage many registered users and requires each \
one to log in, and to produce some form of authentication (usually a \
login name coupled with a password) before allowing the user access \
to system resources."))
  def on_user_login_entry_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Here you must define your login name which should only include \
alphanumeric characters with no space or upper case letters."))
  def on_user_pass1_entry_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Choose a password to be coupled with your login \
name. Your password should include a mix of upper and lower case letters, numbers, \
and even symbols (such as @, !, and &)"))
  def on_user_pass2_entry_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Here you must retype your password as a confirmation \
of your choice."))
  def on_user_visible_checkbutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Check this box if you want to be able to see the password you \
are typing."))
  def on_users_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Create new user."))
  def on_users_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel new user creation."))
  def on_root_pass1_entry_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("On Linux systems, the superuser, or root, is a special user account\
reserved for system administration. Here you must set its password. Remember, \
password should include a mix of upper and lower case letters, numbers, \
and even symbols (such as @, !, and &)"))
  def on_root_pass2_entry_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Here you must retype the superuser (root) password as a \
confirmation of your choice."))
  def on_root_visible_checkbutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Check this box if you want to be able to see the password you \
are typing."))
  def on_rootpass_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Apply new root password."))
  def on_rootpass_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel new root password."))

  # Packages contextual help
  def on_packages_tab_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Access the packages selection."))
  def on_core_radiobutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_markup(_("<b>Core installation:</b>\n\
Only the minimum essentials for a console system to start are \
included. A graphical environment is not provided. This is ideal \
if you are an experienced user and want to customize your \
installation for any specific purpose, such as a web server, \
file server etc."))
  def on_basic_radiobutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_markup(_("<b>Basic installation:</b>\n\
This installs only a basic desktop environment, with very few extra applications \
installed on top, such as a web browser and the gslapt package manager. Ideal \
for advanced users that would like to install a lightweight system and \
add their own choice of applications."))
  def on_full_radiobutton_enter_notify_event(self, widget, data=None):
    if self.cfg.is_liveclone:
      self.ContextLabel.set_markup(_("<b>Full installation:</b>\n\
Salix Live Installer has detected a LiveClone customized environment. \
Core and Basic installation modes are therefore not available. \n\
You can only perform a full installation: all software \
included in your customized LiveClone will be installed."))
    else:
      self.ContextLabel.set_markup(_('<b>Full installation:</b>\n\
Everything that is included in the iso is installed. That includes a complete \
desktop environment and a complete selection of matching applications, \
always following the "one application per task" rationale.'))
  def on_packages_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Confirm your packages selection."))
  def on_packages_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel all packages selection."))

  # Bootloader contextual help
  def on_bootloader_tab_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Access the bootloader selection."))
  def on_nobootloader_radiobutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_markup(_("<b>No bootloader:</b>\n\
This is not recommended unless you already have another bootloader \
and know how to add Salix to it. Salix will not boot without a bootloader."))
  def on_lilo_radiobutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_markup(_("<b>LiLo:</b>\n\
Basic Linux bootloader that simply do the job with a nice graphical menu."))
  def on_grub2_radiobutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_markup(_('<b>Grub2:</b>\n\
Full featured bootloader with editable graphical menu.'))
  def on_bootloader_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Confirm your bootloader selection."))
  def on_bootloader_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel all bootloader selection."))

  # What to do when Salix Installer logo is clicked
  def on_about_link_clicked(self, widget, data=None):
    self.AboutDialog.show()

  # What to do when the about dialog quit button is clicked
  def on_about_dialog_close(self, widget, data=None):
    self.AboutDialog.hide()
    return True

  # What to do when the exit X on the main window upper right is clicked
  def gtk_main_quit(self, widget, data=None):
    print "Bye _o/"
    gtk.main_quit()

  # What to do when the Salix Installer quit button is clicked
  def on_button_quit_clicked(self, widget, data=None):
    self.gtk_main_quit(widget)

  def build_data_stores(self):
    print 'Building choice lists…',
    sys.stdout.flush()
    self.ContinentZoneListStore.clear()
    self.ContinentZoneListStore.append([_("Select...")])
    self.ContinentZoneCombobox.set_active(0)
    for continent in sltl.listTZContinents():
      self.ContinentZoneListStore.append([continent])
    self.CountryZoneListStore.clear()
    self.YearListStore.clear()
    for y in range(2000, 2051):
      self.YearListStore.append([y])
    self.MonthListStore.clear()
    for m in [_('January'), _('February'), _('March'), _('April'), _('May'), _('June'),
        _('July'), _('August'), _('September'), _('October'), _('November'), _('December')]:
      self.MonthListStore.append([m])
    self.DayListStore.clear()
    for d in range(1, 32):
      self.DayListStore.append([d])
    self.KeyboardListStore.clear()
    for km in sltl.listAvailableKeymaps():
      self.KeyboardListStore.append(km)
    self.LocaleListStore.clear()
    for l in sltl.listAvailableLocales():
      self.LocaleListStore.append(l)
    self.MainFormatListStore.clear()
    self.LinuxFormatListStore.clear()
    for f in (('none', _("Do not format")), 'ext2', 'ext3', 'ext4', 'jfs', 'reiserfs', 'xfs'):
      if type(f) is tuple:
        self.MainFormatListStore.append(f)
        self.LinuxFormatListStore.append(f)
      else:
        self.MainFormatListStore.append([f, f])
        self.LinuxFormatListStore.append([f, f])
    self.LinuxMountPointListStore.clear()
    for mp in ('/home', '/tmp', '/usr', '/var', '/mnt/custom', _("Do not mount")):
      self.LinuxMountPointListStore.append([mp])
    self.LinuxNewSysComboCell.set_property("model", self.LinuxFormatListStore)
    self.LinuxNewSysComboCell.set_property('text-column', 1)
    self.LinuxNewSysComboCell.set_property('editable', True)
    self.LinuxNewSysComboCell.set_property('cell-background', '#CCCCCC')
    self.LinuxNewMountComboCell.set_property("model", self.LinuxMountPointListStore)
    self.LinuxNewMountComboCell.set_property('text-column', 0)
    self.LinuxNewMountComboCell.set_property('editable', True)
    self.LinuxNewMountComboCell.set_property('cell-background', '#CCCCCC')
    self.WinMountPointListStore.clear()
    for mp in ('/mnt/windows', '/mnt/xp', '/mnt/vista', '/mnt/seven', '/mnt/win8', '/mnt/data', '/mnt/custom', _("Do not mount")):
      self.WinMountPointListStore.append([mp])
    self.WinMountComboCell.set_property("model", self.WinMountPointListStore)
    self.WinMountComboCell.set_property('text-column', 0)
    self.WinMountComboCell.set_property('editable', True)
    self.WinMountComboCell.set_property('cell-background', '#CCCCCC')
    print ' Done'
    sys.stdout.flush()

  def add_custom_signals(self):
    self.KeyboardList.get_selection().connect('changed', self.on_keyboard_list_changed_event)
    self.LocaleList.get_selection().connect('changed', self.on_locale_list_changed_event)

  def update_install_button(self):
    self.InstallButton.set_sensitive(not False in self.cfg.configurations.values())
  
  def process_gui_events(self):
    """
    be sure to treat any pending GUI events before continue
    """
    while gtk.events_pending():
      gtk.main_iteration()
  
  def update_gui_async(self, fct, *args, **kwargs):
    gobject.idle_add(fct, *args, **kwargs)

  def hide_all_tabs(self):
    self.IntroBox.hide()
    self.TimeBox.hide()
    self.KeyboardBox.hide()
    self.LocaleBox.hide()
    self.PartitioningBox.hide()
    self.MainPartitionBox.hide()
    self.RecapPartitionBox.hide()
    self.UsersBox.hide()
    self.PackagesBox.hide()
    self.BootloaderBox.hide()
    self.TimeTab.set_relief(gtk.RELIEF_NONE)
    self.KeyboardTab.set_relief(gtk.RELIEF_NONE)
    self.LocaleTab.set_relief(gtk.RELIEF_NONE)
    self.PartitionTab.set_relief(gtk.RELIEF_NONE)
    self.UsersTab.set_relief(gtk.RELIEF_NONE)
    self.PackagesTab.set_relief(gtk.RELIEF_NONE)
    self.BootloaderTab.set_relief(gtk.RELIEF_NONE)
  def set_tabs_sensitive(self, sensitive):
    self.TimeTab.set_sensitive(sensitive)
    self.KeyboardTab.set_sensitive(sensitive)
    self.LocaleTab.set_sensitive(sensitive)
    self.PartitionTab.set_sensitive(sensitive)
    self.UsersTab.set_sensitive(sensitive)
    self.PackagesTab.set_sensitive(sensitive)
    self.BootloaderTab.set_sensitive(sensitive)
  def on_time_tab_clicked(self, widget, data=None):
    self.hide_all_tabs()
    self.TimeTab.set_relief(gtk.RELIEF_HALF)
    self.TimeBox.show()
    self.time_settings()
  def on_keyboard_tab_clicked(self, widget, data=None):
    self.hide_all_tabs()
    self.KeyboardTab.set_relief(gtk.RELIEF_HALF)
    self.KeyboardBox.show()
    self.keyboard_settings()
    selection = self.KeyboardList.get_selection().get_selected_rows()[1]
    if selection:
      self.KeyboardList.scroll_to_cell(selection[0], None, True, 0.5)
  def on_locale_tab_clicked(self, widget, data=None):
    self.hide_all_tabs()
    self.LocaleTab.set_relief(gtk.RELIEF_HALF)
    self.LocaleBox.show()
    self.locale_settings()
    selection = self.LocaleList.get_selection().get_selected_rows()[1]
    if selection:
      self.LocaleList.scroll_to_cell(selection[0], None, True, 0.5)
  def on_partition_tab_clicked(self, widget, data=None):
    self.hide_all_tabs()
    self.PartitionTab.set_relief(gtk.RELIEF_HALF)
    self.partitions_settings()
  def on_users_tab_clicked(self, widget, data=None):
    self.hide_all_tabs()
    self.UsersTab.set_relief(gtk.RELIEF_HALF)
    self.UsersBox.show()
    self.users_settings()
  def on_packages_tab_clicked(self, widget, data=None):
    self.hide_all_tabs()
    self.PackagesTab.set_relief(gtk.RELIEF_HALF)
    self.PackagesBox.show()
    self.packages_settings()
  def on_bootloader_tab_clicked(self, widget, data=None):
    self.hide_all_tabs()
    self.BootloaderTab.set_relief(gtk.RELIEF_HALF)
    self.BootloaderBox.show()
    self.bootloader_settings()



  def time_settings(self):
    self.ContinentZoneCombobox.set_active(0)
    index = 1
    for continent in sltl.listTZContinents():
      if continent == self.cfg.cur_tz_continent:
        self.ContinentZoneCombobox.set_active(index)
        break
      index += 1
    self.time_set_cities_list()
    self.NTPCheckButton.set_active(self.cfg.cur_use_ntp)
    self.set_datetime_settings()
    self.ManualTimeBox.set_sensitive(not self.cfg.configurations['time'] and not self.cfg.cur_use_ntp)
    self.NTPCheckButton.set_sensitive(not self.cfg.configurations['time'])
    self.TimeZoneBox.set_sensitive(not self.cfg.configurations['time'])
    self.TimeUndoButton.set_sensitive(self.cfg.configurations['time'])
    self.TimeApplyButton.set_sensitive(not self.cfg.configurations['time'])
    if self.cfg.configurations['time']:
      self.TimeCheck.show()
      self.TimeCheckMarker.hide()
    else:
      self.TimeCheck.hide()
      self.TimeCheckMarker.show()
    self.update_install_button()
  def set_datetime_settings(self):
    corrected_datetime = datetime.now() + self.cfg.cur_time_delta
    year, month, day, hour, minute, second, __, __, __ = corrected_datetime.timetuple()
    index = 0
    for y in self.YearListStore:
      if year == y[0]:
        self.YearCombobox.set_active(index)
        break
      index += 1
    self.MonthCombobox.set_active(month - 1)
    self.DayCombobox.set_active(day - 1)
    self.HourSpinButton.set_value(hour)
    self.MinuteSpinButton.set_value(minute)
    self.SecondSpinButton.set_value(second)
  def time_set_cities_list(self):
    self.CountryZoneListStore.clear()
    self.CountryZoneListStore.append([_("Select...")])
    self.CountryZoneCombobox.set_active(0)
    if self.cfg.cur_tz_continent:
      cities = sltl.listTZCities(self.cfg.cur_tz_continent)
      if cities:
        index = 1
        for city in cities:
          self.CountryZoneListStore.append([city])
          if city == self.cfg.cur_tz_city:
            self.CountryZoneCombobox.set_active(index)
          index += 1
  def on_continent_zone_combobox_changed(self, widget, data=None):
    if self.ContinentZoneCombobox.get_active() > 0:
      continent = self.ContinentZoneCombobox.get_active_text()
      if continent != self.cfg.cur_tz_continent:
        self.cfg.cur_tz_continent = continent
        self.cfg.cur_tz_city = None
    self.time_set_cities_list()
  def on_country_zone_combobox_changed(self, widget, data=None):
    if self.CountryZoneCombobox.get_active() > 0:
      self.cfg.cur_tz_city = self.CountryZoneCombobox.get_active_text()
      self.cfg.cur_tz = self.cfg.cur_tz_continent + '/' + self.cfg.cur_tz_city
  def on_ntp_checkbutton_toggled(self, widget, data=None):
    self.cfg.cur_use_ntp = self.NTPCheckButton.get_active()
    self.set_datetime_settings()
    self.ManualTimeBox.set_sensitive(not self.cfg.cur_use_ntp)
  def on_time_apply_clicked(self, widget, data=None):
    if not self.cfg.cur_use_ntp:
      year = self.YearCombobox.get_active()
      month = self.MonthCombobox.get_active()
      day = self.DayCombobox.get_active()
      hour = int(self.HourSpinButton.get_value())
      minute = int(self.MinuteSpinButton.get_value())
      second = int(self.SecondSpinButton.get_value())
      new_date = datetime(year, month + 1, day + 1, hour, minute, second)
      now = datetime.now()
      self.cfg.cur_time_delta = new_date - now
    else:
      self.cfg.cur_time_delta = timedelta()
    self.cfg.configurations['time'] = True
    self.time_settings()
  def on_time_undo_clicked(self, widget, data=None):
    self.cfg.configurations['time'] = False
    self.time_settings()



  def keyboard_settings(self):
    self.KeyboardSelection.set_text(_('None'))
    if self.cfg.cur_km:
      index = 0
      for km in self.KeyboardListStore:
        if km[0] == self.cfg.cur_km:
          self.KeyboardList.get_selection().select_path(index)
          if self.cfg.configurations['keyboard']:
            self.KeyboardSelection.set_text('{0} ({1})'.format(km[0], km[1]))
          break
        index += 1
    self.NumLockCheckButton.set_active(self.cfg.cur_use_numlock)
    self.IBusCheckButton.set_active(self.cfg.cur_use_ibus)
    self.KeyboardList.set_sensitive(not self.cfg.configurations['keyboard'])
    self.NumLockCheckButton.set_sensitive(not self.cfg.configurations['keyboard'])
    self.IBusCheckButton.set_sensitive(not self.cfg.configurations['keyboard'])
    self.KeyboardUndoButton.set_sensitive(self.cfg.configurations['keyboard'])
    self.KeyboardApplyButton.set_sensitive(not self.cfg.configurations['keyboard'])
    if self.cfg.configurations['keyboard']:
      self.KeyboardCheck.show()
      self.KeyboardCheckMarker.hide()
    else:
      self.KeyboardCheck.hide()
      self.KeyboardCheckMarker.show()
    self.update_install_button()
  def on_keyboard_list_changed_event(self, selection, data=None):
    model, it = selection.get_selected()
    if it:
      self.cfg.cur_km = model.get_value(it, 0)
    else:
      self.cfg.cur_km = None
  def on_numlock_checkbutton_toggled(self, widget, data=None):
    self.cfg.cur_use_numlock = self.NumLockCheckButton.get_active()
  def on_ibus_checkbutton_toggled(self, widget, data=None):
    self.cfg.cur_use_ibus = self.IBusCheckButton.get_active()
  def on_keyboard_apply_clicked(self, widget, data=None):
    if self.cfg.cur_km:
      self.cfg.configurations['keyboard'] = True
      self.keyboard_settings()
  def on_keyboard_undo_clicked(self, widget, data=None):
    self.cfg.configurations['keyboard'] = False
    self.keyboard_settings()



  def locale_settings(self):
    self.LocaleSelection.set_text(_('None'))
    if self.cfg.cur_locale:
      index = 0
      for l in self.LocaleListStore:
        if l[0] + '.utf8' == self.cfg.cur_locale:
          self.LocaleList.get_selection().select_path(index)
          if self.cfg.configurations['locale']:
            self.LocaleSelection.set_text('{0} ({1})'.format(l[0], l[1]))
          break
        index += 1
    self.LocaleList.set_sensitive(not self.cfg.configurations['locale'])
    self.LocaleUndoButton.set_sensitive(self.cfg.configurations['locale'])
    self.LocaleApplyButton.set_sensitive(not self.cfg.configurations['locale'])
    if self.cfg.configurations['locale']:
      self.LocaleCheck.show()
      self.LocaleCheckMarker.hide()
    else:
      self.LocaleCheck.hide()
      self.LocaleCheckMarker.show()
    self.update_install_button()
  def on_locale_list_changed_event(self, selection, data=None):
    model, it = selection.get_selected()
    if it:
      self.cfg.cur_locale = model.get_value(it, 0) + '.utf8'
    else:
      self.cfg.cur_locale = None
  def on_locale_apply_clicked(self, widget, data=None):
    if self.cfg.cur_locale:
      self.cfg.configurations['locale'] = True
      self.locale_settings()
  def on_locale_undo_clicked(self, widget, data=None):
    self.cfg.configurations['locale'] = False
    self.locale_settings()



  def partitions_settings(self):
    self.PartitioningBox.hide()
    self.MainPartitionBox.hide()
    self.LinuxPartitionBox.hide()
    self.WindowsPartitionBox.hide()
    self.RecapPartitionBox.hide()
    self.set_tabs_sensitive(self.cfg.partitions_step in ('none', 'recap'))
    if self.cfg.partitions_step == 'none':
      self.PartitioningBox.show()
    elif self.cfg.partitions_step == 'main':
      self.MainPartitionBox.show()
      self.swap_detection()
    elif self.cfg.partitions_step == 'linux':
      self.LinuxPartitionBox.show()
      self.linux_partition_settings()
    elif self.cfg.partitions_step == 'win':
      self.WindowsPartitionBox.show()
      self.windows_partition_settings()
    elif self.cfg.partitions_step == 'recap':
      self.RecapPartitionBox.show()
      self.recap_partition_settings()
  def on_modify_partition_button_clicked(self, widget, data=None):
    self.Window.set_sensitive(False)
    self.Window.set_accept_focus(False)
    self.Window.hide()
    self.process_gui_events()
    if self.cfg.is_test:
      sltl.execCheck(["/usr/bin/xterm", "-e", 'echo "Gparted simulation run. Please hit enter to continue."; read junk'], shell=False, env=None)
    else:
      sltl.execCheck("/usr/sbin/gparted", shell=False, env=None)
    self.Window.set_sensitive(True)
    self.Window.set_accept_focus(True)
    self.Window.show()
    self.on_do_not_modify_partition_button_clicked(widget)
  def on_do_not_modify_partition_button_clicked(self, widget, data=None):
    self.cfg.partitions_step = 'main'
    self.cfg.main_partition = None
    self.cfg.main_format = None
    self.cfg.linux_partitions = None
    self.cfg.win_partitions = None
    self.partitions_settings()
  def swap_detection(self):
    """
    Displays the swap partitions that were detected on the system which
    will be automatically used by the installer.
    Displays a warning message when no (swap) partition is found.
    """
    try:
      self.cfg.swap_partitions = sltl.getSwapPartitions()
    except subprocess.CalledProcessError as e:
      self.cfg.swap_partitions = []
    swap_info_msg = self.get_swap_partitions_message(True, _("Detected Swap partitions:"),
      _("Salix Live Installer was not able to detect a valid Swap partition on your system.\nA Swap partition could improve overall performances. \
You may want to exit Salix Live Installer now and use Gparted, or any other partitioning tool of your choice, \
to first create a Swap partition before resuming with Salix Live Installer process."))
    info_dialog(swap_info_msg)
    self.main_partition_settings()
  def get_swap_partitions_message(self, full_text, msg_if_found = None, msg_if_not_found = None):
    msg = ''
    if self.cfg.swap_partitions:
      if msg_if_found:
        msg = msg_if_found + "\n"
      for d in self.cfg.swap_partitions:
        if full_text:
          msg += _("{device} will be automatically used as swap.").format(device = "<b>{0}</b>".format(d)) + "\n"
        else:
          msg += '<span foreground="orange" font_family="monospace" weight="bold">- {0}</span>\n'.format(d)
    elif msg_if_not_found:
      msg = msg_if_not_found
    return msg
  def on_external_device_checkbutton_toggled (self, widget, data=None):
    self.cfg.show_external_drives = self.ExternalDeviceCheckButton.get_active()
    self.main_partition_settings()
  def main_partition_settings(self):
    self.cfg.partitions = []
    self.MainPartitionListStore.clear()
    for disk_device in sltl.getDisks():
      disk_info = sltl.getDiskInfo(disk_device)
      if self.cfg.show_external_drives or not disk_info['removable']:
        disk_name = "{0} ({1})".format(disk_info['model'], disk_info['sizeHuman'])
        for p in sltl.getPartitions(disk_device):
          self.cfg.partitions.append(p)
          part_name = p
          part_label = sltl.getFsLabel(p)
          if part_label:
            part_name += " (" + part_label + ")"
          part_size = sltl.getSizes("/dev/" + p)['sizeHuman']
          part_fs = sltl.getFsType(p)
          self.MainPartitionListStore.append([disk_name, part_name, part_size, part_fs, p])
    if self.cfg.main_partition:
      index = 0
      for l in self.MainPartitionListStore:
        if self.cfg.main_partition == l[4]:
          self.MainPartitionList.set_cursor(index)
          break
        index += 1
    index = 0
    for f in self.MainFormatListStore:
      if (self.cfg.main_format and f[0] == self.cfg.main_format) or (not self.cfg.main_format and f[0] == self.cfg.default_format):
        self.MainFormatCombobox.set_active(index)
        break
      index += 1
  def on_main_partition_apply_clicked(self, widget, data=None):
    model_part, it_part = self.MainPartitionList.get_selection().get_selected()
    idx_format = self.MainFormatCombobox.get_active()
    if it_part and idx_format:
      self.cfg.main_partition = model_part.get_value(it_part, 4)
      self.cfg.main_format = self.MainFormatListStore[idx_format][0]
      self.cfg.linux_partitions = []
      self.cfg.win_partitions = []
      self.show_yesno_dialog(self.get_main_partition_message(True), self.on_main_partition_continue, self.on_main_partition_cancel)
  def get_main_partition_message(self, full_text):
    part_name = self.cfg.main_partition
    part_label = sltl.getFsLabel(self.cfg.main_partition)
    if part_label:
      part_name += " (" + part_label + ")"
    if self.cfg.main_format == 'none':
      if full_text:
        msg = _("{device} will be mounted as {mountpoint} without formatting.").format(device = "<b>{0}</b>".format(part_name), mountpoint = "<b>{0}</b>".format('/'))
      else:
        msg = '<span foreground="black" font_family="monospace">- {0} => /</span>'.format(part_name)
    else:
      if full_text:
        msg = _("{device} will be formatted with {fs} and will be mounted as {mountpoint}.").format(device = "<b>{0}</b>".format(part_name), fs = "<b>{0}</b>".format(self.cfg.main_format), mountpoint = "<b>{0}</b>".format('/'))
      else:
        msg = '<span foreground="black" font_family="monospace">- {0} => / (<u>{1}</u>)</span>'.format(part_name, self.cfg.main_format)
    return msg
  def on_main_partition_undo_clicked(self, widget, data=None):
    self.on_main_partition_cancel()
  def on_main_partition_continue(self):
    self.LinuxPartitionListStore.clear()
    self.WindowsPartitionListStore.clear()
    for line in self.MainPartitionListStore:
      p = line[4]
      if p != self.cfg.main_partition:
        disk_name = line[0]
        part_name = line[1]
        part_size = line[2]
        part_fs = line[3]
        if part_fs in ('btrfs', 'ext2', 'ext3', 'ext4', 'reiserfs', 'xfs', 'jfs'):
          self.LinuxPartitionListStore.append([disk_name, part_name, part_size, part_fs, 'none', _("Do not format"), _("Do not mount"), 'gtk-no', 'gtk-edit', p])
        if part_fs in ('ntfs',  'vfat'):
          self.WindowsPartitionListStore.append([disk_name, part_name, part_size, part_fs, _("Do not mount"), 'gtk-edit', p])
    if len(self.LinuxPartitionListStore) > 0:
      self.cfg.partitions_step = 'linux'
    elif len(self.WindowsPartitionListStore) > 0:
      self.cfg.partitions_step = 'win'
    else:
      self.cfg.partitions_step = 'recap'
    self.cfg.linux_partitions = None
    self.cfg.win_partitions = None
    self.partitions_settings()
  def on_main_partition_cancel(self):
    self.cfg.partitions_step = 'none'
    self.cfg.main_partition = None
    self.cfg.main_format = None
    self.cfg.linux_partitions = None
    self.cfg.win_partitions = None
    self.partitions_settings()
  def linux_partition_settings(self):
    pass
  def on_linux_newsys_renderer_combo_editing_started(self, widget, editable, path):
    self.LinuxPartitionApply.set_sensitive(False)
    self.editable_combo = editable # keep it for later
  def on_linux_newsys_renderer_combo_changed(self, widget, path, new_iter):
    e = gtk.gdk.Event(gtk.gdk.FOCUS_CHANGE)
    e.window = self.LinuxPartitionList.window
    e.send_event = True
    e.in_ = False
    self.editable_combo.emit('focus-out-event', e)
  def on_linux_newsys_renderer_combo_edited(self, widget, path, new_text, data=None):
    model = self.LinuxPartitionListStore
    it = model.get_iter(path)
    if new_text == _("Do not format"):
      new_value = 'none'
    else:
      new_value = new_text
    if new_value == 'none':
      model.set_value(it, 7, 'gtk-no')
    else:
      model.set_value(it, 7, 'gtk-yes')
    model.set_value(it, 4, new_value)
    model.set_value(it, 5, new_text)
    self.LinuxPartitionApply.set_sensitive(True)
  def on_linux_newsys_renderer_combo_editing_canceled(self, data=None):
    self.LinuxPartitionApply.set_sensitive(True)
  def on_linux_newmount_renderer_combo_editing_started(self, widget, editable, path):
    self.LinuxPartitionApply.set_sensitive(False)
    self.editable_combo = editable # keep it for later
  def on_linux_newmount_renderer_combo_changed(self, widget, path, new_iter):
    e = gtk.gdk.Event(gtk.gdk.FOCUS_CHANGE)
    e.window = self.LinuxPartitionList.window
    e.send_event = True
    e.in_ = False
    self.editable_combo.emit('focus-out-event', e)
  def on_linux_newmount_renderer_combo_edited(self, widget, path, new_text, data=None):
    model = self.LinuxPartitionListStore
    it = model.get_iter(path)
    if new_text and new_text.startswith('/'):
      model.set_value(it, 8, 'gtk-yes')
    else:
      model.set_value(it, 8, 'gtk-edit')
    model.set_value(it, 6, new_text)
    self.LinuxPartitionApply.set_sensitive(True)
  def on_linux_newmount_renderer_combo_editing_canceled(self, data):
    self.LinuxPartitionApply.set_sensitive(True)
  def on_linux_partition_apply_clicked(self, widget, data=None):
    store = self.LinuxPartitionListStore
    self.cfg.linux_partitions = []
    for l in store:
      p = l[9]
      fs = l[4]
      mp = l[6]
      if mp.startswith('/'): # keep only mounted partitions
        self.cfg.linux_partitions.append([p, fs, mp])
    self.show_yesno_dialog(self.get_linux_partitions_message(True, _("No partition to mount")), self.on_linux_partition_continue, self.on_linux_partition_cancel)
  def get_linux_partitions_message(self, full_text, msg_if_not_found = None):
    msg = ''
    if self.cfg.linux_partitions:
      for part in self.cfg.linux_partitions:
        part_name = part[0]
        part_label = sltl.getFsLabel(part[0])
        if part_label:
          part_name += " (" + part_label + ")"
        if part[1] == 'none':
          if full_text:
            msg += _("{device} will be mounted as {mountpoint} without formatting.").format(device = "<b>{0}</b>".format(part_name), mountpoint = "<b>{0}</b>".format(part[2])) + "\n"
          else:
            msg += '<span foreground="blue" font_family="monospace" weight="bold">- {0} => {1}</span>'.format(part_name, part[2]) + "\n"
        else:
          if full_text:
            msg += _("{device} will be formatted with {fs} and will be mounted as {mountpoint}.").format(device = "<b>{0}</b>".format(part_name), fs = "<b>{0}</b>".format(part[1]), mountpoint = "<b>{0}</b>".format(part[2])) + "\n"
          else:
            msg += '<span foreground="blue" font_family="monospace" weight="bold">- {0} => {2} (<u>{1}</u>)</span>'.format(part_name, part[1], part[2]) + "\n"
    elif msg_if_not_found:
      msg = msg_if_not_found
    return msg
  def on_linux_partition_continue(self):
    if len(self.WindowsPartitionListStore) > 0:
      self.cfg.partitions_step = 'win'
    else:
      self.cfg.partitions_step = 'recap'
    self.partitions_settings()
  def on_linux_partition_cancel(self):
    self.cfg.partitions_step = 'main'
    self.cfg.linux_partitions = None
    self.cfg.win_partitions = None
    self.partitions_settings()
  def windows_partition_settings(self):
    pass
  def on_win_newmount_renderer_combo_editing_started(self, widget, editable, path):
    self.WindowsPartitionApply.set_sensitive(False)
    self.editable_combo = editable # keep it for later
  def on_win_newmount_renderer_combo_changed(self, widget, path, new_iter):
    e = gtk.gdk.Event(gtk.gdk.FOCUS_CHANGE)
    e.window = self.WindowsPartitionList.window
    e.send_event = True
    e.in_ = False
    self.editable_combo.emit('focus-out-event', e)
  def on_win_newmount_renderer_combo_edited(self, widget, path, new_text, data=None):
    model = self.WindowsPartitionListStore
    it = model.get_iter(path)
    if new_text and new_text.startswith('/'):
      model.set_value(it, 5, 'gtk-yes')
    else:
      model.set_value(it, 5, 'gtk-edit')
    model.set_value(it, 4, new_text)
    self.WindowsPartitionApply.set_sensitive(True)
  def on_win_newmount_renderer_combo_editing_canceled(self, data=None):
    self.WindowsPartitionApply.set_sensitive(True)
  def on_windows_partition_apply_clicked(self, widget, data=None):
    store = self.WindowsPartitionListStore
    self.cfg.win_partitions = []
    for l in store:
      p = l[6]
      fs = l[3]
      mp = l[4]
      if mp.startswith('/'): # keep only mounted partitions
        self.cfg.win_partitions.append([p, fs, mp])
    self.show_yesno_dialog(self.get_windows_partitions_message(True, _("No partition to mount")), self.on_windows_partition_continue, self.on_windows_partition_cancel)
  def get_windows_partitions_message(self, full_text, msg_if_not_found = None):
    msg = ''
    if self.cfg.win_partitions:
      for part in self.cfg.win_partitions:
        part_name = part[0]
        part_label = sltl.getFsLabel(part[0])
        if part_label:
          part_name += " (" + part_label + ")"
        if full_text:
          msg += _("{device} will be mounted as {mountpoint} without formatting.").format(device = "<b>{0}</b>".format(part_name), mountpoint = "<b>{0}</b>".format(part[2])) + "\n"
        else:
          msg += '<span foreground="green" font_family="monospace" weight="bold">- {0} => {1}</span>'.format(part_name, part[2]) + "\n"
    elif msg_if_not_found:
      msg = msg_if_not_found
    return msg
  def on_windows_partition_continue(self):
    self.cfg.partitions_step = 'recap'
    self.partitions_settings()
  def on_windows_partition_cancel(self):
    self.cfg.partitions_step = 'main'
    self.cfg.linux_partitions = None
    self.cfg.win_partitions = None
    self.partitions_settings()
  def recap_partition_settings(self):
    self.MainPartRecapLabel.set_markup("<b>{0}</b>".format(self.get_main_partition_message(False).strip()))
    self.LinPartRecapLabel.set_markup("<b>{0}</b>".format(self.get_linux_partitions_message(False, "<i>" + _("No partition") + "</i>").strip()))
    self.WinPartRecapLabel.set_markup("<b>{0}</b>".format(self.get_windows_partitions_message(False, "<i>" + _("No partition") + "</i>").strip()))
    self.SwapPartRecapLabel.set_markup("<b>{0}</b>".format(self.get_swap_partitions_message(False, None ,"<i>" +  _("No partition") + "</i>").strip()))
    self.cfg.configurations['partitions'] = True
    self.PartitionCheck.show()
    self.PartitionCheckMarker.hide()
    self.update_install_button()
  def on_partition_recap_undo_clicked(self, widget, data=None):
    self.cfg.configurations['partitions'] = False
    self.PartitionCheck.hide()
    self.PartitionCheckMarker.show()
    self.update_install_button()
    self.on_main_partition_cancel()



  def users_settings(self):
    if self.cfg.is_liveclone:
      self.CloneLoginEventbox.show()
      self.users_settings_liveclone()
      self.CloneLoginCheckbutton.set_active(self.cfg.keep_live_logins) # raise toggled event
    else:
      self.CloneLoginEventbox.hide()
      self.cfg.configurations['clonelogins'] = True
      self.users_settings_live()
  def users_settings_liveclone(self):
    self.CloneLoginCheckbutton.set_sensitive(not self.cfg.keep_live_logins or not self.cfg.configurations['clonelogins'])
    self.CloneLoginUndo.set_sensitive(self.cfg.keep_live_logins and self.cfg.configurations['clonelogins'])
    self.CloneLoginApply.set_sensitive(self.cfg.keep_live_logins and not self.cfg.configurations['clonelogins'])
    self.update_users_check()
  def users_settings_live(self):
    self.UsersEventbox.set_sensitive(True)
    self.UserLoginEntry.set_text(self.cfg.new_login)
    self.UserLoginEntry.set_sensitive(not self.cfg.configurations['user'])
    self.UserPass1Entry.set_text(self.cfg.new_password)
    self.UserPass1Entry.set_sensitive(not self.cfg.configurations['user'])
    self.UserPass2Entry.set_text(self.cfg.new_password)
    self.UserPass2Entry.set_sensitive(not self.cfg.configurations['user'])
    self.UserVisibleCheckButton.set_sensitive(not self.cfg.configurations['user'])
    self.UsersUndoButton.set_sensitive(self.cfg.configurations['user'])
    self.UsersApplyButton.set_sensitive(not self.cfg.configurations['user'])
    if self.cfg.configurations['user']:
      self.NewUserLogin.set_text(self.cfg.new_login)
    else:
      self.NewUserLogin.set_text(_("None"))
    self.RootPass1Entry.set_text(self.cfg.new_root_password)
    self.RootPass1Entry.set_sensitive(not self.cfg.configurations['root'])
    self.RootPass2Entry.set_text(self.cfg.new_root_password)
    self.RootPass2Entry.set_sensitive(not self.cfg.configurations['root'])
    self.RootVisibleCheckButton.set_sensitive(not self.cfg.configurations['root'])
    self.RootPassUndoButton.set_sensitive(self.cfg.configurations['root'])
    self.RootPassApplyButton.set_sensitive(not self.cfg.configurations['root'])
    if self.cfg.configurations['root']:
      self.RootPassCreated.set_text(_("Yes"))
    else:
      self.RootPassCreated.set_text(_("None"))
    self.update_users_check()
  def update_users_check(self):
    if self.cfg.configurations['clonelogins'] and self.cfg.configurations['user'] and self.cfg.configurations['root']:
      self.UsersCheck.show()
      self.UsersCheckMarker.hide()
    else:
      self.UsersCheck.hide()
      self.UsersCheckMarker.show()
    self.update_install_button()
  def on_clone_login_checkbutton_toggled(self, widget, data=None):
    if self.CloneLoginCheckbutton.get_sensitive():
      self.cfg.keep_live_logins = self.CloneLoginCheckbutton.get_active()
      self.on_clone_login_undo_clicked(None)
      self.on_users_undo_clicked(None)
      self.on_rootpass_undo_clicked(None)
      if self.cfg.keep_live_logins:
        self.cfg.configurations['user'] = True
        self.cfg.configurations['root'] = True
        self.UsersEventbox.set_sensitive(False)
      else:
        self.cfg.configurations['clonelogins'] = True
        self.UsersEventbox.set_sensitive(True)
  def on_clone_login_apply_clicked(self, widget, data=None):
    self.cfg.configurations['clonelogins'] = True
    self.users_settings_liveclone()
  def on_clone_login_undo_clicked(self, widget, data=None):
    self.cfg.configurations['clonelogins'] = False
    self.users_settings_liveclone()
  def get_password_strength(self, pwd):
    """
    Returns tuple containing:
      - a number from 0 to 4 to indicate the strength of the password.
      - a contextual message.
    """
    if not pwd:
      score = 0
      context_msg = ''
    else:
      score = 1
      min_chars = 5
      context_msg = _("Less than {min} characters").format(min = min_chars)
      if len(pwd) >= min_chars:
        score += 1
        context_msg = ''
        if re.search(r'[A-Z]', pwd):
          score += 0.5
        else:
          context_msg += _("No upper case letter...") + "\n"
        if re.search(r'[1-9]', pwd):
          score += 0.5
        else:
          context_msg += _("No number...") + "\n"
        if re.search(r'[-_.,;:!?"\']', pwd):
          score += 0.5
        else:
          context_msg += _("No punctuation...") + "\n"
        if re.search(r'[][(){}/\<>$%*#@^]', pwd):
          score += 0.5
        else:
          context_msg += _("No symbol...") + "\n"
        score = int(math.floor(score))
      if score == 4:
        context_msg = _("Satisfactory!")
    return (score, context_msg)
  def set_progressbar_strength(self, pwd, draw_widget):
    strength, context_msg = self.get_password_strength(pwd)
    gc = draw_widget.window.new_gc()
    bg_color = draw_widget.get_colormap().alloc_color("#FFFFFF")
    border_color = draw_widget.get_colormap().alloc_color("#000000")
    if strength <= 1:
      progress_color = draw_widget.get_colormap().alloc_color("#FF0000")
    elif strength == 2:
      progress_color = draw_widget.get_colormap().alloc_color("#FF8800")
    elif strength == 3:
      progress_color = draw_widget.get_colormap().alloc_color("#CCCC00")
    elif strength == 4:
      progress_color = draw_widget.get_colormap().alloc_color("#00FF00")
    gc.set_foreground(bg_color)
    draw_widget.window.draw_rectangle(gc, True, 0, 1, 80, 20)
    gc.set_foreground(progress_color)
    draw_widget.window.draw_rectangle(gc, True, 0, 1, 20 * strength, 20)
    gc.set_foreground(border_color)
    draw_widget.window.draw_rectangle(gc, False, 0, 1, 80, 20)
    context_label_text = "<b>" + _("Password strength:") + "</b>\n"
    self.ContextLabel.set_markup(context_label_text + context_msg)
  def on_user_pass_strength_expose_event(self, widget, event, data=None):
    if not self.cfg.keep_live_logins:
      self.set_progressbar_strength(self.UserPass1Entry.get_text().strip(), self.UserPassStrength)
  def on_user_pass1_entry_changed(self, widget, data=None):
    self.on_user_pass_strength_expose_event(self, None, None)
  def on_user_visible_checkbutton_toggled(self, widget, data=None):
    self.UserPass1Entry.set_visibility(self.UserVisibleCheckButton.get_active())
    self.UserPass2Entry.set_visibility(self.UserVisibleCheckButton.get_active())
  def check_login(self, login):
    if not login:
      error_dialog(_("Your login name is empty.") + "\n" + _("Please verify and correct!"))
      return False
    elif not re.match(r'^[a-z][-_a-z1-9]*$', login):
      error_dialog(_("Your login name should only contain alphanumeric lowercase characters with no space and should start with a letter.") + "\n" + _("Please verify and correct!"))
      return False
    else:
      return True
  def check_password(self, pwd1, pwd2):
    if not pwd1:
      error_dialog(_("Your password entry is empty.") + "\n" + _("Please verify and correct!"))
      return False
    elif pwd1 != pwd2:
      error_dialog(_("Your two password entries do not match.") + "\n" + _("Please verify and correct!"))
      return False
    else:
      return True
  def on_users_apply_clicked(self, widget, data=None):
    ok = self.check_login(self.UserLoginEntry.get_text().strip())
    if ok:
      ok = self.check_password(self.UserPass1Entry.get_text().strip(), self.UserPass2Entry.get_text().strip())
    if ok:
      self.cfg.configurations['user'] = True
      self.cfg.new_login = self.UserLoginEntry.get_text().strip()
      self.cfg.new_password = self.UserPass1Entry.get_text().strip()
      # got this too for not loosing it while validating the user login and password
      self.cfg.new_root_password = self.RootPass1Entry.get_text().strip()
      self.users_settings_live()
  def on_users_undo_clicked(self, widget, data=None):
    self.cfg.configurations['user'] = False
    self.cfg.new_login = ''
    self.cfg.new_password = ''
    self.users_settings_live()
  def on_root_pass_strength_expose_event(self, widget, event, data=None):
    if not self.cfg.keep_live_logins:
      self.set_progressbar_strength(self.RootPass1Entry.get_text().strip(), self.RootPassStrength)
  def on_root_pass1_entry_changed(self, widget, data=None):
    self.on_root_pass_strength_expose_event(self, None, None)
  def on_root_visible_checkbutton_toggled(self, widget, data=None):
    self.RootPass1Entry.set_visibility(self.RootVisibleCheckButton.get_active())
    self.RootPass2Entry.set_visibility(self.RootVisibleCheckButton.get_active())
  def on_rootpass_apply_clicked(self, widget, data=None):
    ok = self.check_password(self.RootPass1Entry.get_text().strip(), self.RootPass2Entry.get_text().strip())
    if ok:
      self.cfg.configurations['root'] = True
      self.cfg.new_root_password = self.RootPass1Entry.get_text().strip()
      # got this too for not loosing it while validating the root password
      self.cfg.new_login = self.UserLoginEntry.get_text().strip()
      self.cfg.new_password = self.UserPass1Entry.get_text().strip()
      self.users_settings_live()
  def on_rootpass_undo_clicked(self, widget, data=None):
    self.cfg.configurations['root'] = False
    self.cfg.new_root_password = ''
    self.users_settings_live()



  def packages_settings(self):
    self.CoreRadioButton.set_sensitive(not self.cfg.configurations['packages'] and not self.cfg.is_liveclone)
    self.CoreHBox.set_sensitive(not self.cfg.configurations['packages'] and not self.cfg.is_liveclone)
    self.CoreRadioButton.set_active(self.cfg.install_mode == 'Core')
    self.BasicRadioButton.set_sensitive(not self.cfg.configurations['packages'] and not self.cfg.is_liveclone)
    self.BasicHBox.set_sensitive(not self.cfg.configurations['packages'] and not self.cfg.is_liveclone)
    self.BasicRadioButton.set_active(self.cfg.install_mode == 'Basic')
    self.FullRadioButton.set_sensitive(not self.cfg.configurations['packages'])
    self.FullRadioButton.set_active(self.cfg.install_mode == 'Full')
    self.PackagesUndoButton.set_sensitive(self.cfg.configurations['packages'])
    self.PackagesApplyButton.set_sensitive(not self.cfg.configurations['packages'])
    if self.cfg.configurations['packages']:
      self.PackagesCheck.show()
      self.PackagesCheckMarker.hide()
    else:
      self.PackagesCheck.hide()
      self.PackagesCheckMarker.show()
    self.update_install_button()
  def on_packages_apply_clicked(self, widget, data=None):
    if self.CoreRadioButton.get_active():
      self.cfg.install_mode = 'Core'
    elif self.BasicRadioButton.get_active():
      self.cfg.install_mode = 'Basic'
    elif self.FullRadioButton.get_active():
      self.cfg.install_mode = 'Full'
    self.cfg.configurations['packages'] = True
    self.packages_settings()
  def on_packages_undo_clicked(self, widget, data=None):
    self.cfg.install_mode = None
    self.cfg.configurations['packages'] = False
    self.packages_settings()



  def bootloader_settings(self):
    self.NobootloaderRadioButton.set_sensitive(not self.cfg.configurations['bootloader'])
    self.NobootloaderRadioButton.set_active(self.cfg.bootloader == 'none')
    self.LiloRadioButton.set_sensitive(not self.cfg.configurations['bootloader'])
    self.LiloRadioButton.set_active(self.cfg.bootloader == 'lilo')
    self.Grub2RadioButton.set_sensitive(not self.cfg.configurations['bootloader'] and self.cfg.bootsetup_available)
    self.Grub2RadioButton.set_active(self.cfg.bootloader == 'grub2')
    self.BootloaderUndoButton.set_sensitive(self.cfg.configurations['bootloader'])
    self.BootloaderApplyButton.set_sensitive(not self.cfg.configurations['bootloader'])
    if self.cfg.configurations['bootloader']:
      self.BootloaderCheck.show()
      self.BootloaderCheckMarker.hide()
    else:
      self.BootloaderCheck.hide()
      self.BootloaderCheckMarker.show()
    self.update_install_button()
  def on_bootloader_apply_clicked(self, widget, data=None):
    if self.NobootloaderRadioButton.get_active():
      self.cfg.bootloader = 'none'
    elif self.LiloRadioButton.get_active():
      self.cfg.bootloader = 'lilo'
    elif self.Grub2RadioButton.get_active():
      self.cfg.bootloader = 'grub2'
    self.cfg.configurations['bootloader'] = True
    self.bootloader_settings()
  def on_bootloader_undo_clicked(self, widget, data=None):
    self.cfg.bootloader = None
    self.cfg.configurations['bootloader'] = False
    self.bootloader_settings()



  def show_yesno_dialog(self, msg, yes_callback, no_callback):
    self.YesNoDialog.yes_callback = yes_callback
    self.YesNoDialog.no_callback = no_callback
    self.YesNoDialog.set_markup(msg)
    self.YesNoDialog.show()
    self.YesNoDialog.resize(1, 1) # ensure a correct size, by asking a recomputation
  def on_yesno_response(self, dialog, response_id, data=None):
    dialog.hide()
    self.process_gui_events()
    callback = None
    if response_id == gtk.RESPONSE_YES:
      callback = dialog.yes_callback
    elif response_id == gtk.RESPONSE_NO:
      callback = dialog.no_callback
    if callback:
      callback()



  def on_install_button_clicked(self, widget, data=None):
    full_recap_msg = ''
    full_recap_msg += "\n<b>" + _("You are about to install Salix with the following settings:") + "</b>\n"
    full_recap_msg += "\n<b>" + _("Date and Time:") + "</b>\n"
    full_recap_msg += _("- Time zone: {tz}").format(tz = self.cfg.cur_tz) + "\n"
    if self.cfg.cur_use_ntp:
      dt = "NTP"
    else:
      dt = (datetime.now() + self.cfg.cur_time_delta).strftime("%Y-%m-%d %H:%M:%S")
    full_recap_msg += "- Date and time: {dt}\n".format(dt = dt)
    full_recap_msg += "\n<b>" + _("Keyboard:") + "</b>\n"
    full_recap_msg += _("- Layout: {layout}").format(layout = self.KeyboardSelection.get_text()) + "\n"
    if self.cfg.cur_use_numlock:
      nl = '<span style="italic" foreground="green">{0}</span>'.format(_("activated"))
    else:
      nl = '<span style="italic" foreground="maroon">{0}</span>'.format(_("deactivated"))
    if self.cfg.cur_use_ibus:
      ibus = '<span style="italic" foreground="green">{0}</span>'.format(_("activated"))
    else:
      ibus = '<span style="italic" foreground="maroon">{0}</span>'.format(_("deactivated"))
    full_recap_msg += _("- Numlock: {nl}, Ibus: {ibus}").format(nl = nl, ibus = ibus) + "\n"
    full_recap_msg += "\n<b>" + _("System language:") + "</b>\n"
    full_recap_msg += "- {lang}".format(lang = self.LocaleSelection.get_text()) + "\n"
    full_recap_msg += "\n<b>" + _("Partitions:") + "</b>\n"
    part_main = self.get_main_partition_message(False).strip()
    part_linux = self.get_linux_partitions_message(False).strip()
    part_windows =  self.get_windows_partitions_message(False).strip()
    part_swap = self.get_swap_partitions_message(False).strip()
    for p in (part_main, part_linux, part_windows, part_swap):
      if p:
        full_recap_msg += p + "\n"
    if self.cfg.keep_live_logins:
      full_recap_msg += "<b>" + _("Standard User:") + "</b>\n" + _("Using LiveClone login.") + "\n"
    else:
      full_recap_msg += "<b>" + _("Standard User:") + "</b>\n" + self.cfg.new_login + "\n"
    full_recap_msg += "\n<b>" + _("Packages:") + "</b>\n"
    full_recap_msg += _("You have chosen the {mode} installation mode.").format(mode = _(self.cfg.install_mode))
    bootloader = self.cfg.bootloader
    if bootloader == 'none':
      bootloader = _("No bootloader")
    full_recap_msg += _("Bootloader choosen: {bootloader}").format(bootloader = bootloader)
    self.show_yesno_dialog(full_recap_msg, self.install_salixlive, None)
  def install_salixlive(self):
    self.thread_installer = ThreadInstaller(self.cfg, self)
    installation = self.thread_installer.install()
    self.thread_installer = None
    self.installation_umountall()
    if installation == 'done':
      self.installation_postinstall()
  def install_set_main_window_visibility(self, is_shown):
    if is_shown:
      self.Window.set_sensitive(True)
      self.Window.set_accept_focus(True)
      self.Window.show()
    else:
      self.Window.set_sensitive(False)
      self.Window.set_accept_focus(False)
      self.Window.hide()
  def install_set_progress_window_above(self, is_above):
    self.ProgressWindow.set_keep_above(is_above)
  def install_set_progress_window_visibility(self, is_shown):
    if is_shown:
      self.ProgressWindow.show()
    else:
      self.ProgressWindow.hide()
  def install_set_progress_bar_text(self, text):
    self.InstallProgressBar.set_text(text)
  def install_set_progress_bar_fraction(self, fraction):
    self.InstallProgressBar.set_fraction(fraction)
  def install_set_cancel_button_sensitive(self, is_sensitive):
    self.CancelProgressButton.set_sensitive(is_sensitive)
  def on_progress_undo_clicked(self, widget, data=None):
    if self.thread_installer:
      self.thread_installer.cancel()
  def installation_umountall(self):
    if not self.cfg.is_test:
      if self.cfg.linux_partitions:
        for p in self.cfg.linux_partitions:
          d = p[0]
          fulld = "/dev/{0}".format(d)
          if sltl.isMounted(fulld):
            sltl.umountDevice(fulld, deleteMountPoint = False)
      fulld = "/dev/{0}".format(self.cfg.main_partition)
      if sltl.isMounted(fulld):
        sltl.umountDevice(fulld)
  def installation_postinstall(self):
    if self.cfg.bootloader != 'none':
      self.run_bootsetup()
    self.installation_done()
  def run_bootsetup(self):
    if self.cfg.is_test:
      sltl.execCheck(["/usr/bin/xterm", "-e", 'echo "Bootsetup simulation run ({0}). Please hit enter to continue."; read junk'.format(self.cfg.bootloader)], shell=False, env=None)
    else:
      sltl.runBootsetup(self.cfg.bootloader)
  def installation_done(self):
    print "Installation Done.\nHappy Salix."
    msg = "<b>{0}</b>".format(_("Installation process completed successfully..."))
    info_dialog(msg)
    self.gtk_main_quit(self.Window)
