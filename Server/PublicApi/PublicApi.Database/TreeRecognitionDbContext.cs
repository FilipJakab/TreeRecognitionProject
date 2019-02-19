using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;

namespace PublicApi.Database
{
	public partial class TreeRecognitionDbContext : DbContext
	{
		public TreeRecognitionDbContext()
		{
		}

		public TreeRecognitionDbContext(DbContextOptions<TreeRecognitionDbContext> options)
			: base(options)
		{
		}

		public virtual DbSet<ImageDefinition> ImageDefinition { get; set; }
		public virtual DbSet<Metric> Metric { get; set; }
		public virtual DbSet<MetricType> MetricType { get; set; }
		public virtual DbSet<PredictionRequest> PredictionRequest { get; set; }
		public virtual DbSet<PredictionResult> PredictionResult { get; set; }
		public virtual DbSet<WebRequest> WebRequest { get; set; }

		protected override void OnModelCreating(ModelBuilder modelBuilder)
		{
			modelBuilder.Entity<ImageDefinition>(entity =>
			{
				entity.HasKey(e => e.ImageId);

				entity.Property(e => e.ImageId).ValueGeneratedNever();

				entity.Property(e => e.CameraModel).HasMaxLength(20);

				entity.Property(e => e.CameraVendor).HasMaxLength(15);

				entity.Property(e => e.ColorDisposition).HasMaxLength(6);

				entity.Property(e => e.ComponentConfiguration).HasMaxLength(15);

				entity.Property(e => e.Compression).HasMaxLength(20);

				entity.Property(e => e.ExifVersion).HasMaxLength(15);

				entity.Property(e => e.ExposureProgram).HasMaxLength(25);

				entity.Property(e => e.ExposureTime).HasMaxLength(15);

				entity.Property(e => e.FileExtension).HasMaxLength(5);

				entity.Property(e => e.FileName)
					.IsRequired()
					.HasMaxLength(36);

				entity.Property(e => e.Flash).HasMaxLength(30);

				entity.Property(e => e.MakerNote).HasMaxLength(1);

				entity.Property(e => e.Orientation).HasMaxLength(15);

				entity.Property(e => e.OriginalFileName).HasMaxLength(500);

				entity.Property(e => e.ResolutionUnit).HasMaxLength(15);

				entity.Property(e => e.Taken).HasColumnType("date");

				entity.HasOne(d => d.WebRequest)
					.WithMany(p => p.ImageDefinition)
					.HasForeignKey(d => d.WebRequestId)
					.OnDelete(DeleteBehavior.ClientSetNull)
					.HasConstraintName("FK__ImageDefi__WebRe__47DBAE45");
			});

			modelBuilder.Entity<Metric>(entity =>
			{
				entity.Property(e => e.MetricId).ValueGeneratedNever();

				entity.Property(e => e.Ended).HasColumnType("date");

				entity.Property(e => e.MetricCode)
					.IsRequired()
					.HasMaxLength(10);

				entity.Property(e => e.Started).HasColumnType("date");

				entity.HasOne(d => d.MetricCodeNavigation)
					.WithMany(p => p.Metric)
					.HasForeignKey(d => d.MetricCode)
					.OnDelete(DeleteBehavior.ClientSetNull)
					.HasConstraintName("FK__Metric__MetricCo__5629CD9C");

				entity.HasOne(d => d.PredictionRequest)
					.WithMany(p => p.Metric)
					.HasForeignKey(d => d.PredictionRequestId)
					.OnDelete(DeleteBehavior.ClientSetNull)
					.HasConstraintName("FK__Metric__Predicti__5535A963");
			});

			modelBuilder.Entity<MetricType>(entity =>
			{
				entity.HasKey(e => e.Code);

				entity.Property(e => e.Code)
					.HasMaxLength(10)
					.ValueGeneratedNever();

				entity.Property(e => e.Value)
					.IsRequired()
					.HasMaxLength(30);
			});

			modelBuilder.Entity<PredictionRequest>(entity =>
			{
				entity.Property(e => e.PredictionRequestId).ValueGeneratedNever();

				entity.HasOne(d => d.Image)
					.WithMany(p => p.PredictionRequest)
					.HasForeignKey(d => d.ImageId)
					.OnDelete(DeleteBehavior.ClientSetNull)
					.HasConstraintName("FK__Predictio__Image__4AB81AF0");

				entity.HasOne(d => d.WebRequest)
					.WithMany(p => p.PredictionRequest)
					.HasForeignKey(d => d.WebRequestId)
					.OnDelete(DeleteBehavior.ClientSetNull)
					.HasConstraintName("FK__Predictio__WebRe__52593CB8");
			});

			modelBuilder.Entity<PredictionResult>(entity =>
			{
				entity.Property(e => e.PredictionResultId).ValueGeneratedNever();

				entity.Property(e => e.Label)
					.IsRequired()
					.HasMaxLength(30);

				entity.HasOne(d => d.PredictionRequest)
					.WithMany(p => p.PredictionResult)
					.HasForeignKey(d => d.PredictionRequestId)
					.OnDelete(DeleteBehavior.ClientSetNull)
					.HasConstraintName("FK__Predictio__Predi__4D94879B");
			});

			modelBuilder.Entity<WebRequest>(entity =>
			{
				entity.Property(e => e.WebRequestId).ValueGeneratedNever();

				entity.Property(e => e.Requested)
					.HasColumnType("date")
					.HasDefaultValueSql("(getdate())");
			});
		}
	}
}
