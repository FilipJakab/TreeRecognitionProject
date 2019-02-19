using System;
using System.Collections.Generic;

namespace PublicApi.Database
{
    public partial class ImageDefinition
    {
        public ImageDefinition()
        {
            PredictionRequest = new HashSet<PredictionRequest>();
        }

        public int ImageId { get; set; }
        public int WebRequestId { get; set; }
        public string FileName { get; set; }
        public string OriginalFileName { get; set; }
        public string FileExtension { get; set; }
        public int Size { get; set; }
        public string CameraVendor { get; set; }
        public string CameraModel { get; set; }
        public string Orientation { get; set; }
        public DateTime? Taken { get; set; }
        public string Compression { get; set; }
        public int? ResolutionX { get; set; }
        public int? ResolutionY { get; set; }
        public string ResolutionUnit { get; set; }
        public string ExposureTime { get; set; }
        public string ExposureProgram { get; set; }
        public string ExifVersion { get; set; }
        public string ComponentConfiguration { get; set; }
        public double? ExposureBias { get; set; }
        public double? MaxApertureValue { get; set; }
        public string Flash { get; set; }
        public byte[] MakerNote { get; set; }
        public string ColorDisposition { get; set; }
        public int? Width { get; set; }
        public int? Height { get; set; }

        public WebRequest WebRequest { get; set; }
        public ICollection<PredictionRequest> PredictionRequest { get; set; }
    }
}
