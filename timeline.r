# Generate a skills timeline from a CSV of skills and dates

library("reshape2")
library("ggplot2")

# Get skills
skills <- as.data.frame(read.csv("skills.csv"))

# Convert to dates
skills$start <- as.Date(skills$start)
skills$end <- as.Date(skills$end)

# Melt them?
skills_melted <- melt(skills, measure.vars = c("start", "end"))

start_date <- as.Date('1998-09-01')

ggplot(skills_melted, aes(value, name)) +
  geom_line(size = 2) +
  # labs(x = '', y = '', title = "Dean Turpin skills timeline") +
  theme_bw(base_size = 10) +
  theme(plot.title = element_text(hjust = 0.5),
        panel.grid.major.x = element_line(colour="grey", linetype = "dashed"),
        panel.grid.major.y = element_line(colour="grey", linetype = "solid"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.text.x = element_text(angle = 90)) +
  scale_x_date(date_labels = "%Y", limits = c(start_date, NA), date_breaks = '1 year') +
  scale_y_continuous(position = "right")

ggsave("public/skills.png")

