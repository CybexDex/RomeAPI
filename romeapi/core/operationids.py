cybex_ops = [
    "transfer", # replaced by cybex to support vesting transfer
    "limit_order_create",
    "limit_order_cancel", # replaced by cybex to support rte cancel
    "call_order_update",
    "fill_order",
    "account_create",
    "account_update",
    "account_whitelist",
    "account_upgrade",
    "account_transfer",
    "asset_create",
    "asset_update",
    "asset_update_bitasset",
    "asset_update_feed_producers",
    "asset_issue",
    "asset_reserve",
    "asset_fund_fee_pool",
    "asset_settle",
    "asset_global_settle",
    "asset_publish_feed",
    "witness_create",
    "witness_update",
    "proposal_create",
    "proposal_update",
    "proposal_delete",
    "withdraw_permission_create",
    "withdraw_permission_update",
    "withdraw_permission_claim",
    "withdraw_permission_delete",
    "committee_member_create",
    "committee_member_update",
    "committee_member_update_global_parameters",
    "vesting_balance_create",
    "vesting_balance_withdraw",
    "worker_create",
    "custom",
    "assert",
    "balance_claim",
    "override_transfer",
    "transfer_to_blind",
    "blind_transfer",
    "transfer_from_blind",
    "asset_settle_cancel",
    "asset_claim_fees",
    "fba_distribute",

# cybex added operations ################
    "initiate_crowdfund",
    "participate_crowdfund",
    "withdraw_crowdfund",
    "cancel_vesting",
    "fill_crowdfund",
# end cybex added operations ###########

    "bid_collateral",
    "execute_bid",

# rte operation
    "cancel_all",

    "initiate_dice_bet",
    "deposit_dice_bet",
    "withdraw_dice_bet",
    "participate_dice_bet",
    "dice_bet_clearing"
]


operations = {o: cybex_ops.index(o) for o in cybex_ops}
# operations.default_prefix = 'CYB'
