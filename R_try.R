library(ggplot2)
library(data.table)
library(splitstackshape)
library(plotly)


path<-getwd()

deaths_pt<-fread(paste(path,"/Data/Dados_SICO_2020-12-30-Nr_mortes.csv",sep=""),header=TRUE)
total_covid<-fread(paste(path,"/Data/owid-covid-data.csv",sep=""))



# N mortes ----------------------------------------------------------------

deaths_pt_melt<-melt(deaths_pt,id.vars = "Data")

ggplotly(deaths_pt_melt[,.(sum_year=sum(value,na.rm = TRUE)),by=variable]%>%
  ggplot()+
  geom_col(aes(x=variable,y=sum_year))+
    xlab("Year")+
    ylab("Number of Deaths")+
    theme_bw()
    )
#adicionar cor com o numero de mortes covid em 2020


# N mortes vs N casos -----------------------------------------------------
#grafico 4


pt_covid<-total_covid[location=="Portugal"]
pt_covid_month<-cSplit(pt_covid,"date","-",drop=FALSE)
pt_covid_month<-pt_covid_month[,.(cases_month=sum(new_cases,na.rm = TRUE),
                  deaths_month=sum(new_deaths,na.rm = TRUE)
                  ),by=date_2]



month_deaths<-pt_covid_month%>%
  ggplot()+
  geom_col(aes(x=as.factor(date_2),y=deaths_month))+
  geom_vline(xintercept = "3")


month_cases<-pt_covid_month%>%
  ggplot()+
  geom_col(aes(x=as.factor(date_2),y=cases_month))+
  geom_vline(xintercept = "3")


gridExtra::grid.arrange(month_deaths,month_cases)

pt_covid_month_melt<-melt(pt_covid_month,id.vars = "date_2")

pt_covid_month_melt%>%
  ggplot()+
  geom_col(aes(x=date_2,y=value,fill=variable))+
  theme_bw()

