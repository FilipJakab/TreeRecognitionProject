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

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
#warning To protect potentially sensitive information in your connection string, you should move it out of source code. See http://go.microsoft.com/fwlink/?LinkId=723263 for guidance on storing connection strings.
                optionsBuilder.UseSqlServer("Server=localhost;Database=TreeRecognitionDb;User Id=SA;Password=Sel jsem pro modreho slona 2x");
            }
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<ImageDefinition>(entity =>
            {
                entity.Property(e => e.CameraModel).HasMaxLength(20);

                entity.Property(e => e.CameraVendor).HasMaxLength(15);

                entity.Property(e => e.ComponentConfiguration).HasMaxLength(1);

                entity.Property(e => e.Compression).HasMaxLength(20);

                entity.Property(e => e.ExifVersion).HasMaxLength(1);

                entity.Property(e => e.FileName)
                    .IsRequired()
                    .HasMaxLength(36);

                entity.Property(e => e.Orientation).HasMaxLength(15);

                entity.Property(e => e.OriginalFileName).HasMaxLength(500);

                entity.Property(e => e.Taken).HasColumnType("date");

                entity.Property(e => e.Xresolution).HasColumnName("XResolution");

                entity.Property(e => e.Yresolution).HasColumnName("YResolution");

                entity.HasOne(d => d.WebRequest)
                    .WithMany(p => p.ImageDefinition)
                    .HasForeignKey(d => d.WebRequestId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__ImageDefi__WebRe__7A672E12");
            });

            modelBuilder.Entity<Metric>(entity =>
            {
                entity.Property(e => e.Ended).HasColumnType("date");

                entity.Property(e => e.MetricCode)
                    .IsRequired()
                    .HasMaxLength(10);

                entity.Property(e => e.Started).HasColumnType("date");

                entity.HasOne(d => d.MetricCodeNavigation)
                    .WithMany(p => p.Metric)
                    .HasForeignKey(d => d.MetricCode)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__Metric__MetricCo__05D8E0BE");

                entity.HasOne(d => d.WebRequest)
                    .WithMany(p => p.Metric)
                    .HasForeignKey(d => d.WebRequestId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__Metric__WebReque__04E4BC85");
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
                entity.HasOne(d => d.Image)
                    .WithMany(p => p.PredictionRequest)
                    .HasForeignKey(d => d.ImageId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__Predictio__Image__7D439ABD");

                entity.HasOne(d => d.WebRequest)
                    .WithMany(p => p.PredictionRequest)
                    .HasForeignKey(d => d.WebRequestId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__Predictio__WebRe__7E37BEF6");
            });

            modelBuilder.Entity<PredictionResult>(entity =>
            {
                entity.Property(e => e.Label)
                    .IsRequired()
                    .HasMaxLength(30);

                entity.HasOne(d => d.ImageDefinition)
                    .WithMany(p => p.PredictionResult)
                    .HasForeignKey(d => d.ImageDefinitionId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__Predictio__Image__02084FDA");

                entity.HasOne(d => d.PredictionRequest)
                    .WithMany(p => p.PredictionResult)
                    .HasForeignKey(d => d.PredictionRequestId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__Predictio__Predi__01142BA1");
            });

            modelBuilder.Entity<WebRequest>(entity =>
            {
                entity.Property(e => e.Requested)
                    .HasColumnType("date")
                    .HasDefaultValueSql("(getdate())");
            });
        }
    }
}
