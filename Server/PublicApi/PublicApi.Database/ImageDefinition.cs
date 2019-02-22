using System;
using System.Collections.Generic;

namespace PublicApi.Database
{
    public partial class ImageDefinition
    {
        public ImageDefinition()
        {
            PredictionRequest = new HashSet<PredictionRequest>();
            PredictionResult = new HashSet<PredictionResult>();
        }

        public int ImageDefinitionId { get; set; }
        public int? WebRequestId { get; set; }
        public string FileName { get; set; }
        public string OriginalFileName { get; set; }
        public long Size { get; set; }
        public string CameraVendor { get; set; }
        public string CameraModel { get; set; }
        public string Orientation { get; set; }
        public DateTime? Taken { get; set; }
        public string Compression { get; set; }
        public double? Xresolution { get; set; }
        public double? Yresolution { get; set; }
        public short? ResolutionUnit { get; set; }
        public double? ExposureTime { get; set; }
        public short? ExposureProgram { get; set; }
        public byte[] ExifVersion { get; set; }
        public byte[] ComponentConfiguration { get; set; }
        public double? ExposureBias { get; set; }
        public double? MaxApertureValue { get; set; }
        public double? ApertureValue { get; set; }
        public short? Flash { get; set; }
        public short? ColorSpace { get; set; }
        public int? Width { get; set; }
        public int? Height { get; set; }

        public WebRequest WebRequest { get; set; }
        public ICollection<PredictionRequest> PredictionRequest { get; set; }
        public ICollection<PredictionResult> PredictionResult { get; set; }
    }
}
