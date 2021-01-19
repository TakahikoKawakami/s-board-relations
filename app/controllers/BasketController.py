from responder import routes
import logging
import datetime

from app.common.managers import SessionManager

from app.repositories.AccountsRepository import AccountsRepository
from app.repositories.BasketAnalysesRepository import BasketAnalysesRepository
from app.repositories.StoresRepository import StoresRepository
from app.entities.Baskets import Basket
from app.entities.Pyfpgrowth import Pyfpgrowth
from app.forms.BasketForms import BasketForm


class Associate():
    logger = logging.getLogger(__name__)

    accessToken = None
    contractId = None

    async def on_request(self, req, resp):
        self.contractId = SessionManager.getByKey(req.session, SessionManager.KEY_CONTRACT_ID)
        if self.contractId is None:
            resp.redirect('/')
            return
        accountsRepository = AccountsRepository(req.session)
        self.accessToken = accountsRepository.getAccessTokenByContractId(self.contractId, req.session)

    async def on_get(self, req, resp):
        return
        form = BasketForm(request.args, meta={'csrf': False, 'locales':['ja']})
        storesRepository = StoresRepository().withSmaregiApi(accessToken, contractId)
        storeList = storesRepository.getStoreList()
        form.setStoreList(storeList)
        logger.info(storeList)
        resp.html =  api.template(
            'baskets/index.pug',
            contractId = contractId,
            form = form,
            message = "",
            stores = storeList
        )


# @route.route('/summary', methods=['GET'])
# def summary():
#     global accessToken
#     global contractId

#     form = BasketForm(request.args, meta={'csrf': False, 'locales':['ja']})
#     storesRepository = StoresRepository().withSmaregiApi(accessToken, contractId)
#     storeList = storesRepository.getStoreList()
    
#     form.setStoreList(storeList)
#     if not form.validate():
#         message = "validation error"
#         return render_template(
#             'baskets/index.pug',
#             form = form,
#             message = message,
#             stores = storeList
#         )

#     targetStoreId = form.storeField.data
#     targetDateFrom = form.dateFromField.data
#     targetDateTo = form.dateToField.data

#     logger.info("-----search condition-----")
#     logger.info("storeId     : " + targetStoreId)
#     logger.info("search_from : " + targetDateFrom.strftime("%Y-%m-%d"))
#     logger.info("search_to   : " + targetDateTo.strftime("%Y-%m-%d"))

#     # 分析期間の日別バスケットリストを取得
#     basketAnalysesRepository = BasketAnalysesRepository().withSmaregiApi(accessToken, contractId)
#     try:
#         dailyBasketListModelList = basketAnalysesRepository.getDailyBasketListByStoreIdAndAnalysisDateRange(
#             targetStoreId,
#             targetDateFrom,
#             targetDateTo
#         )
#     except Exception as e:
#         logger.error(e.args[0])
#         return redirect(url_for('baskets.index'))

#     # 全データをマージ
#     mergedBasketList = []
#     for dailyBasketListModel in dailyBasketListModelList:
#         mergedBasketList += dailyBasketListModel.basketList
#     mergedPyfpgrowthEntity = Pyfpgrowth.createByDataList(mergedBasketList, 0.1)

#     vis = None
#     if mergedPyfpgrowthEntity is not None:
#         logger.debug("-----merged fpgrowth-----")
#         # logger.debug(mergedPyfpgrowthEntity.patterns)

#         vis = mergedPyfpgrowthEntity.convertToVisJs()
#         # vis = mergedPyfpgrowthEntity.result
    
#     logger.debug("-----analyzed result list-----")
#     logger.debug(vis)
#     #basket.relationRanking("8000002")
    
# #    rules = pyfpgrowth.generate_association_rules(patterns, 0.7)
#     targetStore = storesRepository.getStoreById(targetStoreId) 

#     pickUpProductFrom = None
#     pickUpProductTo = None
#     if (len(mergedPyfpgrowthEntity.result) > 0):
#         pickUpProductFrom = mergedPyfpgrowthEntity.result[0]['from']
#         pickUpProductTo = mergedPyfpgrowthEntity.result[0]['to']
#     pickUpMessage = {
#             'store': targetStore,
#             'from': targetDateFrom,
#             'to': targetDateTo,
#             'productFrom': pickUpProductFrom,
#             'productTo': pickUpProductTo,
#     }

#     return render_template("baskets/summary.pug",
#         contractId = contractId,
#         store = targetStore,
#         search_from = targetDateFrom,
#         search_to = targetDateTo,
#         nodes = vis['nodes'],
#         edges = vis['edges'],
#         pickUpMessage = pickUpMessage
#     )
    

# class BasketScheduler():
#     @staticmethod
#     def syncTodaysBasket():
#         _accountsRepository = AccountsRepository().withSmaregiApi(None, None)
#         _accountList = _accountsRepository.getActiveAccountList()

#         for _account in _accountList:
#             _contractId = _account.contractId
#             result = _accountsRepository.getAccessTokenByContractId(contractId)

#             session['access_token'] = result['access_token']
#             session['access_token_expires_in'] = datetime.datetime.now() + datetime.timedelta(seconds=result['expires_in'])
#         return "hello"