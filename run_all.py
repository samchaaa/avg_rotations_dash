import os
from run_download import check_current
from rotations import get_sign, get_rotations, final
from clean import clean
from write import write, status
from dump import dump_data
from settings import Settings


def get_insts():
    return [x.strip() for x in Settings.INSTS.split('\n') if x != "" and x.strip() != ""]


def update(insts):

    # update all things
    for inst in insts:
        print(inst)
        if inst not in os.listdir(Settings.PATH_DATA):
            os.mkdir('{}/{}'.format(Settings.PATH_DATA, inst))
        check_current(inst)

    # consider making some meta-file that keeps last updated date instead of concatting everytime

    return


def do_thing(inst, interval):

    print("Running calculations: {}".format(inst))
    data = clean(inst, interval)
    data = data['mid']
    data = get_sign(data)
    r = get_rotations(data)
    r = final(inst, r)

    return r


def main():

    status()
    dump_data()

    # Updates everything
    insts = get_insts()
    update(insts)

    for inst in insts:
        r = do_thing(inst, Settings.INTERVAL)
        r.to_csv('{}/{}.csv'.format(Settings.PATH_RESULTS, inst), index=False)

    for inst in insts:
        write(inst, '{}/{}.csv'.format(Settings.PATH_RESULTS, inst))

    status()


if __name__ == '__main__':
    main()

