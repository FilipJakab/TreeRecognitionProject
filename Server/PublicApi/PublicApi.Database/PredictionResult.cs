using System;
using System.Collections.Generic;

namespace PublicApi.Database
{
    public partial class PredictionResult
    {
        public int PredictionResultId { get; set; }
        public int PredictionRequestId { get; set; }
        public int ImageDefinitionId { get; set; }
        public string Label { get; set; }
        public double Score { get; set; }

        public ImageDefinition ImageDefinition { get; set; }
        public PredictionRequest PredictionRequest { get; set; }
    }
}
