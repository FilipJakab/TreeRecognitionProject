using System;
using System.Collections.Generic;

namespace PublicApi.Database
{
    public partial class PredictionImage
    {
        public PredictionImage()
        {
            PredictionResult = new HashSet<PredictionResult>();
        }

        public string FileName { get; set; }

        public ICollection<PredictionResult> PredictionResult { get; set; }
    }
}
