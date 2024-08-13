from pymongo.mongo_client import MongoClient


def get_collection(collection_name="feedback"):
    uri = "mongodb+srv://awei:hww74520i@medicinedata.brcozd9.mongodb.net/?retryWrites=true&w=majority&appName" \
          "=medicineData"

    # Create a new client and connect to the server
    client = MongoClient(uri)
    db = client['medicine_feedback']
    # 获取集合
    collection = db[collection_name]
    return client, collection


def get_batch_data(collection, batch_size=100):
    # 设置每次获取的文档数量
    cursor = collection.find().batch_size(batch_size)
    # print("cursor: ", cursor)

    # 遍历游标
    for document in cursor:
        print(document)


def insert_data_test():
    client, collection = get_collection()
    # 插入文档
    doc = {
        "is_correct": "准确",
        "question": "this is a question",
        "answer": "this is a answer",
        "improve": "this is a improvement"
    }
    insert_result = collection.insert_one(doc)

    # 打印插入文档的 ID
    print(insert_result.inserted_id)
    get_batch_data(collection, 100)
    client.close()


def insert_many_data_test(length=100):
    client, collection = get_collection()
    docs = []
    for i in range(0, length):
        doc = {
            "is_correct": "准确 " + str(i),
            "question": "this is a question " + str(i),
            "answer": "this is a answer " + str(i),
            "improve": "this is a improvement " + str(i)
        }
        docs.append(doc)

    collection.insert_many(docs)
    # 打印插入文档的 ID
    get_batch_data(collection, 100)
    client.close()


def insert_one_data(is_correct, question, answer, improve):
    success = False
    try:
        client, collection = get_collection()
        # 插入文档
        doc = {
            "is_correct": is_correct,
            "question": question,
            "answer": answer,
            "improve": improve
        }
        insert_result = collection.insert_one(doc)
        if insert_result.acknowledged:
            success = True
            print("Insert operation was acknowledged by the server.")

        print(insert_result)
        # 打印插入文档的 ID
        client.close()
    except Exception as e:
        print(e)

    return success


def insert_one_choice(question, answers, choice):
    success = False
    try:
        client, collection = get_collection("choices")
        # 插入文档
        doc = {
            "question": question,
            "answers": answers,
            "choice": choice
        }
        insert_result = collection.insert_one(doc)
        if insert_result.acknowledged:
            success = True
            print("Insert operation was acknowledged by the server.")

        print(insert_result)
        # 打印插入文档的 ID
        client.close()
    except Exception as e:
        print(e)

    return success


def delete_all():
    client, collection = get_collection()
    # 删除集合中的所有文档
    delete_result = collection.delete_many({})
    # 打印删除的文档数量
    print(f"Deleted {delete_result.deleted_count} documents")
    client.close()


if __name__ == '__main__':
    # insert_data_test()
    # insert_many_data_test(1000)
    delete_all()
