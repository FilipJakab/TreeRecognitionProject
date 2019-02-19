using System;
using System.Collections.Generic;

namespace PublicApi.Database
{
    public partial class WebRequest
    {
        public WebRequest()
        {
            ImageDefinition = new HashSet<ImageDefinition>();
            PredictionRequest = new HashSet<PredictionRequest>();
        }

        public int WebRequestId { get; set; }
        public Guid CorrelationId { get; set; }
        public DateTime Requested { get; set; }

        public ICollection<ImageDefinition> ImageDefinition { get; set; }
        public ICollection<PredictionRequest> PredictionRequest { get; set; }
    }
}
