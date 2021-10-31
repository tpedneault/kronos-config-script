var target_dir = installer.value("InstallDir")

function Controller()
{
    installer.setDefaultPageVisible(QInstaller.Introduction, true);

    var page = gui.pageWidgetByObjectName( "ComponentSelectionPage" );
    page.selectComponent( "com.msys2.root" );
    page.selectComponent( "com.msys2.root.base" );

    installer.setDefaultPageVisible(QInstaller.ComponentSelection, false);
    installer.setDefaultPageVisible(QInstaller.StartMenuSelection, false);
    installer.setDefaultPageVisible(QInstaller.LicenseCheck, false);
    installer.setDefaultPageVisible(QInstaller.ReadyForInstallation, false);
    installer.setDefaultPageVisible(QInstaller.PerformInstallation, true);
    installer.setDefaultPageVisible(QInstaller.InstallationFinished, true);
    installer.setDefaultPageVisible(QInstaller.FinishedPage, true);
    ComponentSelectionPage.selectAll();
    installer.autoRejectMessageBoxes();
    var result = QMessageBox.question("quit.question", "Installer", "Do you want to quit the installer?",
                                      QMessageBox.Yes | QMessageBox.No);
 
    installer.setMessageBoxAutomaticAnswer("OverwriteTargetDirectory", QMessageBox.Yes);
    installer.setMessageBoxAutomaticAnswer("stopProcessesForUpdates", QMessageBox.Ignore);
}

Controller.prototype.IntroductionPageCallback = function()
{
    gui.clickButton(buttons.NextButton);
}

Controller.prototype.TargetDirectoryPageCallback = function()
{
    gui.currentPageWidget().TargetDirectoryLineEdit.setText(target_dir);
    gui.clickButton(buttons.NextButton);
}

Controller.prototype.StartMenuDirectoryPageCallback = function()
{
    gui.clickButton(buttons.NextButton);
}

Controller.prototype.PerformInstallationPageCallback = function()
{
    var page = gui.pageWidgetByObjectName("PerformInstallationPage");
    installer.setAutomatedPageSwitchEnabled(true);
    gui.clickButton(buttons.NextButton);
}

Controller.prototype.InstallationFinishedPageCallback = function()
{
    var checkBox = gui.pageWidgetByObjectName("RunItCheckBox");

    var page = gui.pageWidgetByObjectName("InstallationFinishedPage");
    gui.clickButton(buttons.NextButton);
}

Controller.prototype.FinishedPageCallback = function()
{
    var page = gui.pageWidgetByObjectName("FinishedPage");
    page.RunItCheckBox.checked = false;
    gui.clickButton(buttons.FinishButton);
}