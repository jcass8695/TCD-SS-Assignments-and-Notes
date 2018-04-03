alter table SuperPerson
drop constraint FK_HideoutID;

alter table SuperPerson
drop constraint FK_NemesisID;

alter table Sidekick
drop constraint FK_MentorID;

alter table Powers
drop constraint FK_PowersSuperID;

alter table HeroDisaster
drop constraint FK_HeroID;

alter table HeroDisaster
drop constraint FK_HeroEventID;

alter table VillianDisaster
drop constraint FK_VillianID;

alter table VillianDisaster
drop constraint FK_VillianEventID;

alter table Equipment
drop constraint FK_OwnerID;

alter table OriginStory
drop constraint FK_OriginStorySuperID;
