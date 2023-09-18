from django.urls import path, include
# from . import views_daily
from . import views_reg
from . import views_for
from django.contrib.auth import views as auth_views
from .Dash_app import stock_dashboard
from .Dash_app import simpleexample
from .Dash_app import Eod_Market_Stock_New
from .Dash_app import Intraday_Option_Chart
from .Dash_app import Eod_Option_Chart
# from . import simpleexample
# from . import stock_dashboard
# from . import live_option_chart_ne
# from . import Eod_Market_Stock_New


urlpatterns = [
    
    path("", views_reg.home, name='home'),
    path("home1", views_reg.home1, name='home1'),
    path("home2", views_reg.home2, name='home2'),
    path("About", views_reg.About, name='About'),
    path("About1", views_reg.About1, name='About1'),
    path("Services", views_reg.Services, name='Services'),
    path("Services1", views_reg.Services1, name='Services1'),
    path("Portfolio", views_reg.Portfolio, name='Portfolio'),
    path("Portfolio1", views_reg.Portfolio1, name='Portfolio1'),
    path("PortfolioDeatils", views_reg.PortfolioDeatils, name='PortfolioDeatils'),    
    path("PortfolioDeatils1", views_reg.PortfolioDeatils1, name='PortfolioDeatils1'),
    path("Team", views_reg.Team, name='Team'),
    path("Team1", views_reg.Team1, name='Team1'),
    path("Blog", views_reg.Blog, name='Blog'),
    path("Blog1", views_reg.Blog1, name='Blog1'),
    path("BlogDetails", views_reg.BlogDetails, name='BlogDetails'),
    path("BlogDetails1", views_reg.BlogDetails1, name='BlogDetails1'),
    path("Contactus", views_reg.Contactus, name='Contactus'),
    path("Contactus1", views_reg.Contactus1, name='Contactus1'),
    path("password_reset/",auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name="password_reset"),
    path("password_reset/done/",auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
	path("password-reset-confirm/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name="password_reset_confirm"),
	path("password-reset-complete/",auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name="password_reset_complete"),    
    path("login_view", views_reg.login_view, name='login_view'),
    path("Register_new", views_reg.Register_new, name='Register_new'),
    path("resend_otp", views_reg.resend_otp, name='resend_otp'),
    path("PagesLogin", views_reg.PagesLogin, name='PagesLogin'),
    path("PagesRegister", views_reg.PagesRegister, name='PagesRegister'),
    path("profile", views_reg.profile, name='profile'),
    path("exxit", views_reg.exxit, name='exxit'),

    path("Analysis", views_for.Analysis, name='Analysis'),
    path("Chart", views_for.Chart, name='Chart'),
    path("Chart1", views_for.Chart1, name='Chart1'),
    path("live_option_chart", views_for.live_option_chart, name='live_option_chart'),
    path("Eod_Market", views_for.Eod_Market, name='Eod_Market'),
    path("Eod_Market_Stock", views_for.Eod_Market_Stock, name='Eod_Market_Stock'),
    path("Eod_Market_Stock_New", views_for.Eod_Market_Stock_New, name='Eod_Market_Stock_New'),
    path("Eod_Market_Indices", views_for.Eod_Market_Indices, name='Eod_Market_Indices'),
    path("Eod_Market_Futures", views_for.Eod_Market_Futures, name='Eod_Market_Futures'),
    path("Eod_Market_Options", views_for.Eod_Market_Options, name='Eod_Market_Options'),
    path("Eod_Market_FII_DII", views_for.Eod_Market_FII_DII, name='Eod_Market_FII_DII'),
    path("Eod_Stock_Chart", views_for.Eod_Stock_Chart, name='Eod_Stock_Chart'),
    path("Eod_Indices_Chart", views_for.Eod_Indices_Chart, name='Eod_Indices_Chart'),
    path("Eod_Option_Chart", views_for.Eod_Option_Chart, name='Eod_Option_Chart'),

    path("Intraday_Market", views_for.Intraday_Market, name='Intraday_Market'),
    path("Intraday_Market_Stock", views_for.Intraday_Market_Stock, name='Intraday_Market_Stock'),
    path("Intraday_Market_Indices", views_for.Intraday_Market_Indices, name='Intraday_Market_Indices'),
    path("Intraday_Market_Futures", views_for.Intraday_Market_Futures, name='Intraday_Market_Futures'),
    path("Intraday_Market_Options", views_for.Intraday_Market_Options, name='Intraday_Market_Options'),
    path("Intraday_Market_FII_DII", views_for.Intraday_Market_FII_DII, name='Intraday_Market_FII_DII'),
    path("Intraday_Option_Chart", views_for.Intraday_Option_Chart, name='Intraday_Option_Chart'),

    path("Backtest", views_for.Backtest, name='Backtest'),
    path("Backtest_Stock", views_for.Backtest_Stock, name='Backtest_Stock'),
    path("Backtest_Indices", views_for.Backtest_Indices, name='Backtest_Indices'),
    path("Backtest_Futures", views_for.Backtest_Futures, name='Backtest_Futures'),
    path("Backtest_Options", views_for.Backtest_Options, name='Backtest_Options'),
    path("Backtest_FII_DII", views_for.Backtest_FII_DII, name='Backtest_FII_DII'),

    path("News", views_for.News, name='News'),
    path("News_India", views_for.News_India, name='News_India'),
    path("News_World", views_for.News_World, name='News_World'),
    path("News_Top", views_for.News_Top, name='News_Top'),
    path("News_Latest", views_for.News_Latest, name='News_Latest'),
    path("News_Most_Readed", views_for.News_Most_Readed, name='News_Most_Readed'),

    path("welcome", views_for.welcome, name='welcome'),
    path("stock_dashboard", views_for.stock_dashboard, name='stock_dashboard'),
    #path("live_option_chart_new", views_for.live_option_chart_new, name='live_option_chart_new'),


    # path("bhavcopy", views_daily.bhavcopy, name='bhavcopy'),
    # path("bhavcopy_fno", views_daily.bhavcopy_fno, name='bhavcopy_fno'),
    # path("fii_openint_down", views_daily.fii_openint_down, name='fii_openint_down'),
    # path("fii_vol_down", views_daily.fii_vol_down, name='fii_vol_down'),
    # path("expirt_date", views_daily.expirt_date, name='expirt_date'),
    # path("live_option_chain", views_daily.live_option_chain, name='live_option_chain'),
   
]

