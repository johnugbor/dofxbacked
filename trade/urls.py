from django.urls import path

from .views import CheckBalance, DepositAmount, WithdrawAmount, ListTransactions, ProcessWithdrawal, BuyOrder, \
    SellOrder, OpenPosition, ClosedPosition, ClosePosition, FinancePanel, AssetView

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
    # Process withdraw `amount` from transaction
    path('wallet/process_withdrawal/', ProcessWithdrawal.as_view(), name='process-withdraw'),

    path('buy/', BuyOrder.as_view(), name='buy'),
    path('sell/', SellOrder.as_view(), name='sell'),
    path('openposition/', OpenPosition.as_view(), name='openposition'),
    path('closedposition/', ClosedPosition.as_view(), name='closedposition'),
    path('closeposition/', ClosePosition.as_view(), name='closeposition'),
    path('financepanel/', FinancePanel.as_view(), name='financepanel'),
    path('assets/', AssetView.as_view(), name='assets')

]
