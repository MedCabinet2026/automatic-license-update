insert_user_query = """insert Users (UserLogin, UserPassword, UserIsNT, UserDepartmentRef, UserName, UserSpecialityRef, UserIsScheduled, UserShortName, UserTitle, UserIsDisabled, UserIsPatient, UserPatientRef, UserULC, UserDLC, UserCreationDate, UserCreationUser, UserCompanyGUID, UserUsesSCH, UserSettingXMLArchived, UseUserSetting, UserPhone, UserDocumentNumber, UserDocumentType, UserPersonalNumber, UserDisplayLogin, UserIsOther, UsersDLC, UserOrder, UserIsExternal, UserDesc, UserLevelRef, UserEmail, UserNameL1, UserNameL2, UserNameL3, UserNameL4, UserNameL5, UserCardNumber, UserPhoto, UserSecurityIdentifier, UserDefaultTimeTableKindRef, UserSpecialityCertificateNumber, UserSpecialityCertificateExpirationDate, UserBirthDate)
values (N'bohdan',cast (pwdencrypt ('ukr2505') as nvarchar (200)),N'0',N'1',N'Ковба Богдан', null,N'0',N'Ковба Б.І.',N'',N'0',N'0', null,N'Administrator',getdate(),getdate(),N'Administrator', null, null, null,N'0',N'', null, null, null, null,N'0',getdate(), null,N'0', null, null, null, null, null, null, null, null, null, null, null, null, null, null, null)

insert into UserRoleGrant
values ('bohdan', N'Права - Керівник','bohdan', getdate (), getdate (),'bohdan')
 
insert into UserRoleGrant
values ('bohdan', N'Права - Повний контроль','bohdan', getdate (), getdate (),'bohdan')
insert into UserRoleGrant
values ('bohdan', N'Права - Всі','bohdan', getdate (), getdate (),'bohdan')
insert into UserRoleGrant
values ('bohdan', N'Шаблони - Всі','bohdan', getdate (), getdate (),'bohdan')
insert into UserRoleGrant
values ('bohdan', N'Права - Керівник','bohdan', getdate (), getdate (),'bohdan')

insert into UserRole
    select 'bohdan', N'Права - Повний контроль',getdate () union all
    select 'bohdan', N'Права - Всі',getdate () union all
    select 'bohdan', N'Шаблони - Всі',getdate () union all
    select 'bohdan', N'Права - Керівник',getdate ()"""