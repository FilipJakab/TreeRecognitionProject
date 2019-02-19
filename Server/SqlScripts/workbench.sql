use TreeRecognitionDb;

create table dbo.MetricType (
  Code nvarchar(10) not null primary key,
  Value nvarchar(30) not null
);

create table dbo.WebRequest (
  WebRequestId int not null primary key,
  CorrelationId uniqueidentifier not null,
	Requested date not null default getdate()
);

create table dbo.ImageDefinition (
	ImageId int not null primary key,
	WebRequestId int not null foreign key references dbo.WebRequest(WebRequestId),
	FileName nvarchar(36) not null,
	OriginalFileName nvarchar(500),
	FileExtension nvarchar(5),
	Size int not null,
	-- exif data
	CameraVendor nvarchar(15),
	CameraModel nvarchar(20),
	Orientation nvarchar(15),
	Taken date,
	Compression nvarchar(20),
	ResolutionX int,
	ResolutionY int,
	ResolutionUnit nvarchar(15),
	ExposureTime nvarchar(15),
	ExposureProgram nvarchar(25),
	ExifVersion nvarchar(15),
	ComponentConfiguration nvarchar(15),
	ExposureBias float,
	MaxApertureValue float,
	Flash nvarchar(30),
	MakerNote binary,
	ColorDisposition nvarchar(6),
	Width int,
	Height int,
);

create table dbo.PredictionRequest (
	PredictionRequestId int not null primary key,
	ImageId int not null foreign key references dbo.ImageDefinition(ImageId)
);

create table dbo.PredictionResult (
	PredictionResultId int not null primary key,
	PredictionRequestId int not null foreign key references dbo.PredictionRequest(PredictionRequestId),
	Label nvarchar(30) not null,
	Score float not null
);

create table dbo.Metric (
	MetricId int not null primary key,
	PredictionRequestId int not null foreign key references dbo.PredictionRequest(PredictionRequestId),
	MetricCode nvarchar(10) not null foreign key references dbo.MetricType(Code),
	Started date not null,
	Ended date not null,
);

drop table dbo.Metric
