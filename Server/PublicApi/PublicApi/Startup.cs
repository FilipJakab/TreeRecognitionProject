using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.HttpOverrides;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using PublicApi.Database;
using PublicApi.Interfaces;
using PublicApi.Managers;
using PublicApi.Models;
using PublicApi.Models.Base;
using PublicApi.Models.Configurations;
using PublicApi.Models.Interfaces;
using PublicApi.Providers;

namespace PublicApi
{
	public class Startup
	{
		public IConfiguration Configuration { get; }

		public Startup(IConfiguration configuration)
		{
			Configuration = configuration;
		}

		// This method gets called by the runtime. Use this method to add services to the container.
		public void ConfigureServices(IServiceCollection services)
		{
			services.AddOptions();
			services.Configure<Urls>(Configuration.GetSection("Urls"));
			services.Configure<Paths>(Configuration.GetSection("Paths"));

			// For linux's reversed proxy..
			services.Configure<ForwardedHeadersOptions>(opts =>
			{
				opts.ForwardedHeaders = ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto;
			});

			services.AddDbContext<TreeRecognitionDbContext>(opts =>
				opts.UseSqlServer(Configuration.GetConnectionString("TreeRecognitionDb")));

			services.AddTransient<IImageManager, ImageManager>();
			services.AddTransient<IHttpProvider, HttpProvider>();
			services.AddTransient<IDatabaseProvider, TreeRecognitionDbProvider>();
//			services.AddTransient<IDatabaseProvider, TreeRecognitionDbProvider>(provider =>
//			{
//				Guid correlationId = Guid.NewGuid();
//
//				TreeRecognitionDbContext dbContext = provider.GetService<TreeRecognitionDbContext>();
//				ILogger<BaseDatabaseProvider> logger = provider.GetService<ILogger<BaseDatabaseProvider>>();
//
//				return new TreeRecognitionDbProvider(correlationId, dbContext, logger);
//			});

			services.AddMvc()
				.AddJsonOptions(opts =>
					opts.SerializerSettings.ReferenceLoopHandling = ReferenceLoopHandling.Ignore)
				.SetCompatibilityVersion(CompatibilityVersion.Version_2_1);
		}

		// This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
		public void Configure(IApplicationBuilder app, IHostingEnvironment env)
		{
			if (env.IsDevelopment())
			{
				app.UseDeveloperExceptionPage();
			}
			else
			{
				app.UseHsts();
			}

			//app.UseHttpsRedirection();
			app.UseMvc();
		}
	}
}
