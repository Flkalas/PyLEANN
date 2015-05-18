# def mergeConnectedGraph(listSetSimilarity):            
#     numConfirm = 0
#     listToNext = listSetSimilarity
#     
#     while numConfirm != len(listToNext):
#         listToMerge = listToNext
#         listToNext = []
#         numConfirm = 0
#                                     
#         waitSetList = [True for _ in range(len(listToMerge))]
#         
#         for i,setBased in enumerate(listToMerge):
#             for j, setTargeted in enumerate(listToMerge):
#                 if waitSetList[i] and waitSetList[j] and i != j:
#                     if len(setTargeted & setBased) > 0:
#                         listToNext.append(setTargeted|setBased)
#                         waitSetList[i] = False
#                         waitSetList[j] = False
#                         break
#             if waitSetList[i]:
#                 listToNext.append(setBased)
#                 waitSetList[i] = False
#                 numConfirm += 1
#                 
#     return listToNext
# 
# a = [{0,4},{0,5},{1,2},{5,6}]
# print mergeConnectedGraph(a)


