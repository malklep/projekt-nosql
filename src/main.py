from store import Store
import pprint

def main():
    store = Store()

    print(store.put('test', 'wartość'))
    print(store.put('inny klucz', 'inna wartość'))
    print(store.put('test', 'zmiana wartości', namespace='osiolek'))
    print(store.put('test', 'zmiana'))

    x = store.get('test')
    print(x)
    print(store.put('test', 'kolejna wartość', guard=x['guard']))

    pprint.pprint(store._store)

    os = store.get('test', namespace='osiolek')
    result = store.delete('test', namespace='osiolek', guard=os['guard'])
    print(result)
    pprint.pprint(store._store)

    store.save()

if __name__ == '__main__':
    main()