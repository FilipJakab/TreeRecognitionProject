using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using Flurl;
using Flurl.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using PublicApi.Interfaces;
using PublicApi.Services;

namespace PublicApi.Providers
{
	public class HttpProvider : IHttpProvider
	{
		private readonly ILogger<HttpProvider> logger;
		private readonly Guid correlationId;

		public HttpProvider(ILogger<HttpProvider> logger, CorrelationService correlationService)
		{
			this.logger = logger;
			correlationId = correlationService.CorrelationId;
		}

		/// <summary>
		/// Posts file stream to specified url.
		/// Expects a json response
		/// </summary>
		/// <param name="url"></param>
		/// <param name="data"></param>
		/// <returns>Deserialized JSON response into T</returns>
		public async Task<T> PostAsync<T>(string url, object data)
		{
			logger.LogTrace($"{correlationId} - Sending POST request to {url}");

			HttpResponseMessage httpResponseMessage = await url.PostJsonAsync(data);

			return JsonConvert.DeserializeObject<T>(await httpResponseMessage.Content.ReadAsStringAsync());
		}

		public async Task<T> GetAsync<T>(string url, Dictionary<string, string> requestArgs)
		{
			logger.LogTrace($"{correlationId} - Sending GET request to url: {url}");

			Url request = new Url(url);
			foreach (KeyValuePair<string, string> kvp in requestArgs)
				request.SetQueryParam(kvp.Key, kvp.Value);
			
			string response = await request
				.GetStringAsync();
			
			return JsonConvert.DeserializeObject<T>(response);
		}
	}
}
