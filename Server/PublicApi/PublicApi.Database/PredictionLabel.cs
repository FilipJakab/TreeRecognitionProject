using System;
using System.Collections.Generic;

namespace PublicApi.Database
{
    public partial class PredictionLabel
    {
        public PredictionLabel()
        {
            PredictionResult = new HashSet<PredictionResult>();
        }

        public int LabelId { get; set; }
        public string LabelName { get; set; }

        public ICollection<PredictionResult> PredictionResult { get; set; }
    }
}
