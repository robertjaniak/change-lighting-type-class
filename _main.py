import vs

new_class = 'Spot'
symbol_list = set()
dialog_id = None


def execute():

    if create_dialog():
        vs.ForEachObject(add_to_list, 'SEL')
        for h in symbol_list:
            vs.ForEachObjectInList(change_attributes, 0, 1, vs.FInSymDef(h))
        vs.DSelectAll()
        vs.DoMenuTextByName('Refresh Instruments', 0)


def add_to_list(h):
    symbol_name = vs.GetRField(h, 'Lighting Device', 'Symbol Name')
    symbol_list.add(vs.GetObject(symbol_name))


def change_attributes(h):
    object_class = vs.GetClass(h)
    rules = [vs.GetTypeN(h) != 11,
             object_class != 'Lighting-Movement Radius',
             object_class != 'Lighting-Parts-Lense',
             object_class != 'Lighting-Input-3D',
             object_class != 'Lighting-Input-2D']
    if all(rules):
        vs.SetPenColorByClass(h)
        vs.SetClass(h, 'Lighting-Type-' + new_class)


def create_dialog():
    global dialog_id
    dialog_id = vs.CreateLayout('Change Fixture Class', False, 'Apply', 'Cancel')
    vs.CreateStaticText(dialog_id, 4, 'Lighting-Type-', -1)
    vs.CreateEditText(dialog_id, 6, new_class, 20)
    vs.SetFirstLayoutItem(dialog_id, 4)
    vs.SetRightItem(dialog_id, 4, 6, 0, 0)
    return vs.RunLayoutDialog(dialog_id, dialog_handler)


def dialog_handler(item, _data):
    global new_class
    if item == 1:
        new_class = vs.GetItemText(dialog_id, 6)
    return item
