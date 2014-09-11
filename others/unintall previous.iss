[Setup]
AppName=My Program
AppVersion=1.5
AppId=1C9FAC66-219F-445B-8863-20DEAF8BB5CC
DefaultDirName={pf}\My Program
OutputDir=userdocs:Inno Setup Examples Output

[CustomMessages]
OptionsFormCaption=Setup options...
RepairButtonCaption=Repair
UninstallButtonCaption=Uninstall

[Code]
const
  mrRepair = 100;
  mrUninstall = 101;

function ShowOptionsForm: TModalResult;
var
  OptionsForm: TSetupForm;
  RepairButton: TNewButton;
  UninstallButton: TNewButton;
begin
  Result := mrNone;
  OptionsForm := CreateCustomForm;
  try
    OptionsForm.Width := 220;
    OptionsForm.Caption := ExpandConstant('{cm:OptionsFormCaption}');
    OptionsForm.Position := poScreenCenter;

    RepairButton := TNewButton.Create(OptionsForm);
    RepairButton.Parent := OptionsForm;
    RepairButton.Left := 8;
    RepairButton.Top := 8;
    RepairButton.Width := OptionsForm.ClientWidth - 16;
    RepairButton.Caption := ExpandConstant('{cm:RepairButtonCaption}');
    RepairButton.ModalResult := mrRepair;

    UninstallButton := TNewButton.Create(OptionsForm);
    UninstallButton.Parent := OptionsForm;
    UninstallButton.Left := 8;
    UninstallButton.Top := RepairButton.Top + RepairButton.Height + 8;
    UninstallButton.Width := OptionsForm.ClientWidth - 16;
    UninstallButton.Caption := ExpandConstant('{cm:UninstallButtonCaption}');
    UninstallButton.ModalResult := mrUninstall;

    OptionsForm.ClientHeight := RepairButton.Height + UninstallButton.Height + 24;
    Result := OptionsForm.ShowModal;
  finally
    OptionsForm.Free;
  end;
end;

function GetUninstallerPath: string;
var
  RegKey: string;
begin
  Result := '';
  RegKey := Format('%s\%s_is1', ['Software\Microsoft\Windows\CurrentVersion\Uninstall', 
    '{#emit SetupSetting("AppId")}']);
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE, RegKey, 'UninstallString', Result) then
    RegQueryStringValue(HKEY_CURRENT_USER, RegKey, 'UninstallString', Result);
end;

function InitializeSetup: Boolean;
var
  UninstPath: string;
  ResultCode: Integer;  
begin
  Result := True;
  UninstPath := RemoveQuotes(GetUninstallerPath);
  if UninstPath <> '' then
  begin
    case ShowOptionsForm of
      mrRepair: Result := True;
      mrUninstall: 
      begin
        Result := False;
        if not Exec(UninstPath, '', '', SW_SHOW, ewNoWait, ResultCode) then
          MsgBox(FmtMessage(SetupMessage(msgUninstallOpenError), [UninstPath]), mbError, MB_OK);
      end;
    else
      Result := False;
    end;
  end;
end;