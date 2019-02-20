using System;

namespace PublicApi.Services
{
	public class CorrelationService
	{
		public Guid CorrelationId { get; }

		public CorrelationService()
		{
			CorrelationId = Guid.NewGuid();
		}
	}
}
