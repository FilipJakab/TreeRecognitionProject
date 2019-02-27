use TreeRecognitionDb;

create table dbo.MetricType (
  Code nvarchar(10) not null primary key,
  Value nvarchar(30) not null
);

create table dbo.WebRequest (
  WebRequestId int identity(1, 1) not null primary key,
  CorrelationId uniqueidentifier not null,
	Requested date not null default getdate()
);

create table dbo.ImageDefinition (
	ImageDefinitionId int identity(1, 1) not null primary key,
	WebRequestId int foreign key references dbo.WebRequest(WebRequestId),
	FileName nvarchar(50) not null,
	OriginalFileName nvarchar(500),
	Size bigint not null,
	-- exif data
	CameraVendor nvarchar(30),
	CameraModel nvarchar(30),
	Orientation nvarchar(30),
	Taken date,
	Compression nvarchar(30),
	XResolution float,
	YResolution float,
	ResolutionUnit smallint,
	ExposureTime float,
	ExposureProgram smallint,
	ExifVersion varbinary(500),
	ComponentConfiguration varbinary(500),
	ExposureBias float,
	MaxApertureValue float,
	ApertureValue float,
	Flash smallint,
	ColorSpace smallint,
	Width int,
	Height int,
);

create table dbo.PredictionRequest (
	PredictionRequestId int identity(1, 1) not null primary key,
	ImageDefinitionId int not null foreign key references dbo.ImageDefinition(ImageDefinitionId) on delete cascade,
	WebRequestId int not null foreign key references dbo.WebRequest(WebRequestId) on delete cascade
);

create table dbo.PredictionResult (
	PredictionResultId int identity(1, 1) not null primary key,
	PredictionRequestId int not null foreign key references dbo.PredictionRequest(PredictionRequestId),
	ImageDefinitionId int not null foreign key references dbo.ImageDefinition(ImageDefinitionId),
	Label nvarchar(30) not null,
	Score float not null
);

create table dbo.Metric (
	MetricId int identity(1, 1) not null primary key,
	WebRequestId int not null foreign key references dbo.WebRequest(WebRequestId) on delete cascade,
	MetricCode nvarchar(10) not null foreign key references dbo.MetricType(Code),
	Started date not null,
	Ended date not null,
);

-- alter table dbo.ImageDefinition
-- 	drop column Size
--
-- alter table dbo.ImageDefinition
-- 	drop column FileExtension
--
-- alter table dbo.ImageDefinition
-- 	add Size bigint not null
--
-- alter table dbo.PredictionRequest
-- 	add WebRequestId int not null foreign key references dbo.WebRequest(WebRequestId)
--
-- drop table dbo.Metric

-- drop table dbo.Metric
--
-- alter table dbo.ImageDefinition
-- 	drop column MakerNote

-- select * from ImageDefinition
-- select * from PredictionRequest
-- select * from PredictionResult
-- select * from Metric
--
select *
from dbo.WebRequest w
-- inner join dbo.ImageDefinition d on w.WebRequestId = d.WebRequestId
--
-- delete from dbo.WebRequest

alter table dbo.ImageDefinition
	alter column ComponentConfiguration varbinary(500)

alter table dbo.ImageDefinition
	alter column ExifVersion varbinary(500)

insert into dbo.MetricType (Code, Value) values ('OVERALL', '')
