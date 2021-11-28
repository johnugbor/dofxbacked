from django.urls import path

from .views import CheckBalance, DepositAmount, WithdrawAmount, ListTransactions,ProcessWithdrawal


urlpatterns = [

    # List Wallet transactions
    path('wallet/<int:pk>/transactions/', ListTransactions.as_view(),
         name='list-transactions'),

    # Get wallet balance value.
    path('wallet/balance/', CheckBalance.as_view(), name='get-balance'),

    # Deposit `amount` to wallet
    path('wallet/deposit/', DepositAmount.as_view(), name='deposit'),

    # Withdraw `amount` from wallet
    path('wallet/withdraw/', WithdrawAmount.as_view(), name='withdraw'),
    #Process withdraw `amount` from transaction
    path('wallet/process_withdrawal/', ProcessWithdrawal.as_view(), name='process-withdraw'),
   



]
