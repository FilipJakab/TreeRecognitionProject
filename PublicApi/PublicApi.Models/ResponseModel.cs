using System;

namespace PublicApi.Models
{
	public sealed class ResponseModel<T>
	{
		public bool IsOk { get; set; }

		public string ErrorMessage { get; set; } = null;

		public Exception Exception { get; set; } = null;

		public Metrics Metrics { get; set; }

		public T Data { get; set; }
	}
}
