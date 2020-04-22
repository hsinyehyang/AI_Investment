# ===================================================================================
# =========================================================================== Library
# ===================================================================================
library(quantmod)
# ===================================================================================
# ========================================================================== Function
# ===================================================================================

Function_Update_TW_Stock_PriceData = function(
  	Git_path,
	Project_nm = 'AI_Investment',
	Save_Data_Path, 
	Work_Dir
){

dir.create(Save_Data_Path)

data.colname.vt = c('Open', 'High', 'Low', 'Close', 'Volume', 'Adjusted')
code.vt1 = paste0(read.csv(paste0(Git_path, Project_nm, '/TW_Stock_Code1.csv'), 
				  stringsAsFactors = F)$Code, '.TW')
code.vt2 = paste0(read.csv(paste0(Git_path, Project_nm, '/TW_Stock_Code2.csv'), 
				  stringsAsFactors = F)$Code, '.TWO')
code.vt  = gsub(' ', '', c(code.vt1, code.vt2))

MaxDate.vt = sapply(code.vt, function(code.c){
	#browser()
	code = strsplit(code.c, "[.]")[[1]][1]
	file.name = paste0('TW_Stock_', code)
	if(file.exists(paste0(Save_Data_Path, file.name, '.csv'))){
		old.data.df = read.csv(paste0(Save_Data_Path, file.name, '.csv'), stringsAsFactors = F)
		LastDate = tail(old.data.df$Date, 1)
		FromDate = as.Date(LastDate)+1
		stock.data = try(getSymbols(code.c, auto.assign = FALSE, from = FromDate))
		if(class(stock.data) != 'try-error'){
			#browser()
			stock.df = as.data.frame(stock.data)
			colnames(stock.df) = data.colname.vt
			stock.df = cbind('Date' = rownames(stock.df), stock.df)
			rownames(stock.df) = NULL
			new.data.df = rbind(old.data.df, stock.df)
			colnames(new.data.df) = c('Date', data.colname.vt)
		}
		else{
			new.data.df = old.data.df
			colnames(new.data.df) = c('Date', data.colname.vt)
		}
		write.csv(new.data.df, paste0(Save_Data_Path, file.name, '.csv'), row.names = F)
		as.character(tail(stock.df$Date, 1))
	}
	else{
		stock.data = try(getSymbols(code.c, auto.assign = FALSE, from = '2000-01-01"'))
		if(class(stock.data) != 'try-error'){
			#browser()
			stock.df = as.data.frame(stock.data)
			colnames(stock.df) = data.colname.vt
			stock.df = cbind('Date' = rownames(stock.df), stock.df)
			rownames(stock.df) = NULL
			write.csv(stock.df, paste0(Save_Data_Path, file.name, '.csv'), row.names = F)
			as.character(tail(stock.df$Date, 1))
		}
		else{
			NA
		}
	}
})
write.csv(cbind('Code' = names(MaxDate.vt), 'LastDate' = MaxDate.vt), 
          paste0(Git_path, Project_nm, Work_Dir, '/TW_Stock_LastDateCheck.csv'), row.names = F)


}
# ===================================================================================