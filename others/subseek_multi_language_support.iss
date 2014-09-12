
#define MyAppName "My Program"

[Setup]
AppName={#MyAppName}
AppVersion=1.6
AppId=1C9FAC66-219F-445B-8863-20DEAF8BB5CC
DefaultDirName={pf}\My Program
OutputDir=userdocs:Inno Setup Examples Output






[Code]

type 
  line_arr  = array of string;

var
  Button: TNewButton;
  ComboBox: TNewComboBox;
  CheckBox1: TNewCheckBox;
  CheckBox2: TNewCheckBox;
  CustomPage: TWizardPage; 
  fileName: string; 
  lines : line_arr;
 
procedure DisableNextButton();
begin
  WizardForm.NextButton.Enabled := False;
  WizardForm.Update;
end; 
  
procedure EnableNextButton();
begin
  WizardForm.NextButton.Enabled := True;
  WizardForm.Update;
end;

procedure CurPageChanged(CurPageID: Integer);
  begin
  if CurPageID = CustomPage.ID then begin
    // always disable the cancel button; no going back now!!!
    DisableNextButton();
  end;
end;

procedure FileWrite(lang: string);
begin                              	
  fileName := ExpandConstant('{pf}\{#MyAppName}\configuration.xml');
  SetArrayLength(lines, 9);
  lines[0] := '<?xml version="1.0" encoding="utf-8"?>';
  lines[1] := '<subseeek>';
  lines[2] := '<subtitleLanguage>';
  lines[3] :=  lang;
  lines[4] := '</subtitleLanguage>';
  lines[5] := '<updateCheck>';
  lines[6] := '1';
  lines[7] := '</updateCheck>';
  lines[8] := '</subseeek>' ;
  SaveStringsToFile(filename,lines,false);
end;

procedure ComboBoxChange(Sender: TObject);
begin
  EnableNextButton();
  case ComboBox.ItemIndex of
    0:
    begin
      FileWrite('ara');
    end;
    1:
    begin
     FileWrite('asm');
    end;
    2:
    begin
      FileWrite('ben');
    end;
    3:
    begin
      FileWrite('chi');
    end;

    4:
    begin
      FileWrite('cze');
    end;

    5:
    begin
      FileWrite('dan');
    end;

    6:
    begin
      FileWrite('eng');
    end;

    7:
    begin
      FileWrite('fre');
    end;

    8:
    begin
      FileWrite('ger');
    end;

    9:
    begin
      FileWrite('guj');
    end;

    10:
    begin
      FileWrite('hin');
    end;

    11:
    begin
      FileWrite('ind');
    end;

    12:
    begin
      FileWrite('ita');
    end;

    13:
    begin
      FileWrite('jpn');
    end;


    14:
    begin
      FileWrite('kan');
    end;

    15:
    begin
     FileWrite('kas');
    end;

    16:
    begin
      FileWrite('kor');
    end;
    17:
    begin
      FileWrite('mar');
    end;

    18:
    begin
      FileWrite('mni');
    end;

    19:
    begin
      FileWrite('nep');
    end;

    20:
    begin
      FileWrite('por');
    end;

    21:
    begin
      FileWrite('raj');
    end;

    22:
    begin
      FileWrite('rus');
    end;

    23:
    begin
      FileWrite('spa');
    end;

    24:
    begin
      FileWrite('tel');
    end;


    25:
    begin
      FileWrite('rum');
    end;

    26:
    begin
      FileWrite('pob');
    end;

  end;
end;



procedure InitializeWizard;
var
  DescLabel: TLabel;
begin
  
  

  CustomPage := CreateCustomPage(wpSelectDir  , 'Choose your language in which you want your subtitle to be downloaded', 'Your subtitle will be downloaded in the prefered language in which you have choosen..');

  DescLabel := TLabel.Create(WizardForm);
  DescLabel.Parent := CustomPage.Surface;
  DescLabel.Left := 0;
  DescLabel.Top := 0;
  DescLabel.Caption := 'Select prefered language for your subtitle..';

  ComboBox := TNewComboBox.Create(WizardForm);
  ComboBox.Parent := CustomPage.Surface;
  ComboBox.Left := 0;
  ComboBox.Top := DescLabel.Top + DescLabel.Height + 6;  
  ComboBox.Width := 190;
  ComboBox.Style := csDropDownList;
  ComboBox.Items.Add('Arabic');
  ComboBox.Items.Add('Assamese');
  ComboBox.Items.Add('Bengali');
  ComboBox.Items.Add('Chinese	');
  ComboBox.Items.Add('Czech	');
  ComboBox.Items.Add('Danish	');
  ComboBox.Items.Add('English	');
  ComboBox.Items.Add('French	');
  ComboBox.Items.Add('German	');
  ComboBox.Items.Add('Gujarati	');
  ComboBox.Items.Add('Hindi	');
  ComboBox.Items.Add('Indonesian	');
  ComboBox.Items.Add('Italian	');
  ComboBox.Items.Add('Japanese	');
  ComboBox.Items.Add('Kannada		');
  ComboBox.Items.Add('Kashmiri');
  ComboBox.Items.Add('Korean		');
  ComboBox.Items.Add('Marathi		');
  ComboBox.Items.Add('Manipuri	');
  ComboBox.Items.Add('Nepali');
  ComboBox.Items.Add('Portuguese');
  ComboBox.Items.Add('Rajasthani');
  ComboBox.Items.Add('Russian');
  ComboBox.Items.Add('Spanish	');
  ComboBox.Items.Add('Telugu	');
  ComboBox.Items.Add('Romanian	');
  ComboBox.Items.Add('Brazilian');

  ComboBox.OnChange := @ComboBoxChange;
  
end;



/////////////////////////////////////////////////////////////////////
function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{#emit SetupSetting("AppId")}_is1');
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;


/////////////////////////////////////////////////////////////////////
function IsUpgrade(): Boolean;
begin
  Result := (GetUninstallString() <> '');
end;


/////////////////////////////////////////////////////////////////////
function UnInstallOldVersion(): Integer;
var
  sUnInstallString: String;
  iResultCode: Integer;
begin
// Return Values:
// 1 - uninstall string is empty
// 2 - error executing the UnInstallString
// 3 - successfully executed the UnInstallString

  // default return value
  Result := 0;

  // get the uninstall string of the old app
  sUnInstallString := GetUninstallString();
  if sUnInstallString <> '' then begin
    sUnInstallString := RemoveQuotes(sUnInstallString);
    if Exec(sUnInstallString, '/SILENT /NORESTART /SUPPRESSMSGBOXES','', SW_HIDE, ewWaitUntilTerminated, iResultCode) then
      Result := 3
    else
      Result := 2;
  end else
    Result := 1;
end;

/////////////////////////////////////////////////////////////////////
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if (CurStep=ssInstall) then
  begin
    if (IsUpgrade()) then
    begin
      UnInstallOldVersion();
    end;
  end;
end;