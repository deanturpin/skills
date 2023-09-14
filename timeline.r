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
  # Plot y axis labels on right
  scale_y_discrete(position = "right") +
  # Set title size
  theme(plot.title = element_text(size = 8)) +
  # Add today's date as the title
  labs(x = '', y='', title = format(Sys.Date(), "Updated %B %Y")) +
  theme(plot.title = element_text(hjust = 0.5),
        panel.grid.major.x = element_line(colour="grey", linetype = "dashed"),
        panel.grid.major.y = element_line(colour="grey", linetype = "solid"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.text.x = element_text(angle = 90)) +
  scale_x_date(date_labels = "%Y", limits = c(start_date, NA), date_breaks = '1 year')

ggsave("public/skills.png")

