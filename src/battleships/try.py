# list = [1, 2, 3, 4]
# print(list)
# new_list = []
# for i, x in enumerate(list):
#     print(x, i)
#     while x > 0:
#         new_list.append(4 - i)
#         x -= 1
# print(new_list)
# list = [1, 2, 3, 4]
# # list2 = [False for x in range(sum(list))]
#
#
# # list = [1, 2, 3, 4]
# # i = 4
# # list2 = [i - x for x in list]
#
# print(list[-1])
# list_of_ships = [[5, 8, 2, 8, 2, 1],
#                  [5, 8, 2, 8, 2, 2],
#                  [5, 8, 2, 8, 2, 3],
#                  [5, 8, 2, 8, 2, 77]
#                  ]
#
# key = list_of_ships[-1][5]
# list_of_ships.append([3, 4, 5, 8, 1, key + 1])
# print(list_of_ships)
# for i, list1 in enumerate(list_of_ships):
#     print(i, list1)

# string = "hello : people : all"
# val = string.split(" :", )
# print(val)

# list = []
# del list
# list = ["1", "2"]
#
# print(list)

# players = {"p1": "player1", "p2": "player2"}
# print(players)
# turn = "player1"
# if turn == players["p1"]:
#     print("True")

# string = "gsfdhg"
# if string[0] == 'g':
#     print(string[0])

# list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# print(len(list1))
# print(list(enumerate(list1, 1))[-1][0])

# l1 = ["eat", "sleep", "repeat"]
#
# # printing the tuples in object directly
# for ele in enumerate(l1):
#     print(ele)
list_of_ships = [[5, 8, 2, 8, 2, 1], [5, 8, 2, 8, 2, 2], [5, 8, 2, 8, 2, 3], [5, 8, 2, 8, 2, 77]]
# for hit_ship, ship in enumerate(list_of_ships):
#     if ship[5] == 2:
#         print(hit_ship)
if 5 in (list_of_ships[0], list_of_ships[1]):
    print("True")
