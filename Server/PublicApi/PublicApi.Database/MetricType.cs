using System;
using System.Collections.Generic;

namespace PublicApi.Database
{
    public partial class MetricType
    {
        public MetricType()
        {
            Metric = new HashSet<Metric>();
        }

        public string Code { get; set; }
        public string Value { get; set; }

        public ICollection<Metric> Metric { get; set; }
    }
}
