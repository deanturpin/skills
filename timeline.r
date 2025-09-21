# Generate a skills timeline from a CSV of skills and dates

library("reshape2")
library("ggplot2")

# Load and prepare data
skills <- read.csv("skills.csv", stringsAsFactors = FALSE)
skills$start <- as.Date(skills$start)
skills$end <- as.Date(skills$end)

# Reshape for plotting
skills_melted <- melt(skills, measure.vars = c("start", "end"))

# Set consistent start date
start_date <- as.Date('1998-09-01')

# Create the timeline plot
ggplot(skills_melted, aes(x = value, y = reorder(name, desc(name)))) +
  geom_line(linewidth = 1.5, colour = "#2C3E50", alpha = 0.8) +
  scale_y_discrete(position = "right") +
  scale_x_date(
    date_labels = "%Y",
    limits = c(start_date, NA),
    date_breaks = '2 years',
    expand = c(0.02, 0)
  ) +
  labs(
    x = "",
    y = "",
    title = format(Sys.Date(), "Skills Timeline • Updated %B %Y")
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(
      size = 10,
      hjust = 0.5,
      colour = "#2C3E50",
      margin = margin(b = 20)
    ),
    axis.text.x = element_text(
      angle = 45,
      hjust = 1,
      size = 8,
      colour = "#34495E"
    ),
    axis.text.y = element_text(
      size = 7,
      colour = "#34495E"
    ),
    panel.grid.major.x = element_line(
      colour = "#BDC3C7",
      linetype = "dotted",
      linewidth = 0.5
    ),
    panel.grid.major.y = element_line(
      colour = "#ECF0F1",
      linewidth = 0.3
    ),
    panel.grid.minor = element_blank(),
    plot.background = element_rect(fill = "white", colour = NA),
    panel.background = element_rect(fill = "white", colour = NA)
  )

# Save with improved quality
ggsave("public/skills.png", width = 12, height = 8, dpi = 300, bg = "white")

