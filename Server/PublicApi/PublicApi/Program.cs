using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Serilog;

namespace PublicApi
{
	public class Program
	{
		public static IConfiguration Configuration { get; } = new ConfigurationBuilder()
			.SetBasePath(Directory.GetCurrentDirectory())
			.AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
			.AddJsonFile($"appsettings.{Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT") ?? "Production"}.json",
				optional: true)
			.AddJsonFile("ConnectionStrings.json", false)
			.AddJsonFile("Keys.json", false)
			.AddEnvironmentVariables()
			.Build();

		public static void Main(string[] args)
		{
			var webHost = BuildWebHost(args);

			var logger = webHost.Services.GetRequiredService<ILogger<Program>>();
			logger.LogInformation("WebHost was built and is about to run.");

			webHost.Run();
		}

		private static IWebHost BuildWebHost(string[] args)
		{
			IWebHostBuilder webHostBuilder = WebHost.CreateDefaultBuilder(args)
				.UseStartup<Startup>()
				.UseSerilog(ConfigureSerilog); // Serilog usage as the logging provider

			IWebHost webHost = webHostBuilder.Build();
			return webHost;
		}

		private static void ConfigureSerilog(WebHostBuilderContext context, LoggerConfiguration loggerConfiguration)
		{
			loggerConfiguration.ReadFrom.Configuration(context.Configuration);
			Serilog.Debugging.SelfLog.Enable(Console.Error);
		}
	}
}
