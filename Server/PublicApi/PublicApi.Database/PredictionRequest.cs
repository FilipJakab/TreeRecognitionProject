using System;
using System.Collections.Generic;

namespace PublicApi.Database
{
    public partial class PredictionRequest
    {
        public PredictionRequest()
        {
            PredictionResult = new HashSet<PredictionResult>();
        }

        public int PredictionRequestId { get; set; }
        public int ImageDefinitionId { get; set; }
        public int WebRequestId { get; set; }

        public ImageDefinition ImageDefinition { get; set; }
        public WebRequest WebRequest { get; set; }
        public ICollection<PredictionResult> PredictionResult { get; set; }
    }
}
