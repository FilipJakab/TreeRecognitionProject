using System;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
using Flurl;
using Flurl.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace PublicApi.Providers
{
	public class HttpProvider
	{
		private readonly ILogger<HttpProvider> logger;

		public HttpProvider(ILogger<HttpProvider> logger)
		{
			this.logger = logger;
		}

		/// <summary>
		/// Posts file stream to specified url.
		/// Expects a json response
		/// </summary>
		/// <param name="correlationId"></param>
		/// <param name="url"></param>
		/// <param name="fileStream"></param>
		/// <param name="fileName"></param>
		/// <returns></returns>
		public async Task<T> PostStream<T>(Guid correlationId, string url, Stream fileStream, string fileName)
		{
			logger.LogTrace($"{correlationId} - Sending streamed content with fileName: {fileName} to url: {url} ");

			HttpResponseMessage httpResponseMessage = await url.PostMultipartAsync(content =>
				content.AddFile("image", fileStream, fileName));

			return JsonConvert.DeserializeObject<T>(await httpResponseMessage.Content.ReadAsStringAsync());
		}
	}
}