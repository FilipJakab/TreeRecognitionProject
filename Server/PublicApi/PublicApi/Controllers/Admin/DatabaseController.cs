using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using Microsoft.AspNetCore.Cors;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using PublicApi.Database;

namespace PublicApi.Controllers.Admin
{
	/// <summary>
	/// Serves as API endpoint which should return 'raw' data (for example from database)
	/// </summary>
	[Route("api/admin/database")]
	[EnableCors("AllowedOriginsPolicy")]
	public class DatabaseController : ControllerBase
	{
		private List<PropertyInfo> getContextProperties;

		private List<PropertyInfo> contextProperties =>
			getContextProperties ?? (getContextProperties = context
				.GetType()
				.GetProperties()
				.Where(prop => prop.PropertyType.IsGenericType &&
				               prop.PropertyType == typeof(DbSet<>).MakeGenericType(prop.PropertyType.GenericTypeArguments))
				.ToList());

		private readonly ILogger<DatabaseController> logger;
		private readonly TreeRecognitionDbContext context;

		public DatabaseController(ILogger<DatabaseController> logger, TreeRecognitionDbContext context)
		{
			this.logger = logger;
			this.context = context;
		}

		[HttpGet("gettables")]
		public IActionResult GetTables()
		{
			List<string> tableNames = new List<string>();

			foreach (PropertyInfo property in contextProperties)
			{
				string name = property.Name,
					nameLower = property.Name.ToLower();
				if (nameLower.EndsWith("dbcontext") || nameLower == "model" || nameLower == "database" ||
				    nameLower == "changetracker")
					continue;

				tableNames.Add(name);
			}

			return Ok(tableNames);
		}

		[HttpGet("gettabledata")]
		public IActionResult GetTableData(string tableName)
		{
			PropertyInfo requestedTableProperty = contextProperties.FirstOrDefault(field =>
				field.Name.ToLower().Equals(tableName.ToLower()));

			if (requestedTableProperty == null)
				return NotFound("Table was not found");

			// Retrieve .ToList Method
			MethodInfo toListMethodInfo = typeof(Enumerable)
				.GetMethods(BindingFlags.Public | BindingFlags.Static)
				.First(method => method.Name == "ToList");
			MethodInfo genericToList =
				toListMethodInfo.MakeGenericMethod(requestedTableProperty.PropertyType.GenericTypeArguments);

			return Ok(genericToList.Invoke(null, new[] {requestedTableProperty.GetValue(context)}));
		}
	}
}
