import os
import json
import argparse
import logging
import paths
from rich import console
from httpx import ConnectError
from innertube.clients import InnerTube
from innertube.errors import RequestError
from typecheck import check_container, compare_container
from utils import get_innertube_data, get_terminal_dimensions

from typing import (
    Tuple,
    Dict,
    Callable,
    List,
    Optional
)

from innertube_de import (
    InnerTubeDE,
    ExtractionError,
    Container,
    CardShelf
)


logging.basicConfig(
    level=logging.DEBUG, 
    format="[%(asctime)s %(levelname)s in %(module)s]: %(message)s"
)
log = logging.getLogger(__name__)
cs = console.Console()


class Tester:
    def __init__(
            self, 
            innertube: InnerTube,
            target: paths.Target,
            verbose: bool = False, 
            save_data: bool = True,
            log_errors: bool = True,
            stack_info: bool = True,
            exc_info: bool = True,
            enable_exceptions: bool = True,
            include_all_urls: bool = True
    ) -> None:

        self.target = target
        self.innertube = innertube
        self.extractor = InnerTubeDE(
            log_errors=log_errors,
            stack_info=stack_info,
            exc_info=exc_info,
            enable_exceptions=enable_exceptions,
            include_all_urls=include_all_urls
        )

        self.ext_log: List[str] = []  # extraction log
        self.ser_log: List[str] = []  # serialization log
        self.des_log: List[str] = []  # deserialization log
        self.dat_log: List[str] = []  # data integrity log

        self.ext_containers: Dict[str, Optional[Container]] = {}  # extracted containers
        self.ser_containers: Dict[str, Optional[Dict]] = {}       # serialized containers
        self.des_containers: Dict[str, Optional[Container]] = {}  # deserialized containers

        self.save_data = save_data
        self.verbose = verbose

        with open(paths.TEST_DATA, mode="r") as file:
            test_data = json.loads(file.read())

        target_tests = test_data[target.value]
        self.test_sear = target_tests["sear"]  # search tests
        self.test_brow = target_tests["brow"]  # browse tests
        self.test_next = target_tests["next"]  # next tests

        if self.target == paths.Target.YOUTUBE:
            self.dump_path = paths.TEST_YT_DUMP
            self.inne_path = paths.TEST_YT_INNT
            self.errs_path = paths.TEST_YT_ERRS
        else:
            self.dump_path = paths.TEST_YM_DUMP
            self.inne_path = paths.TEST_YM_INNT
            self.errs_path = paths.TEST_YM_ERRS


    def test_search_extraction(self) -> None:
        for test in self.test_sear:
            self._do_extraction_test(
                func=lambda: self.innertube.search(
                    query=test["query"],
                    params=test["params"],
                    continuation=test["continuation"],
                ),
                test_type="sear",
                test_name=test["name"],
            )

    def test_browse_extraction(self) -> None:
        for test in self.test_brow:
            self._do_extraction_test(
                func=lambda: self.innertube.browse(
                    browse_id=test["browse_id"],
                    params=test["params"],
                    continuation=test["continuation"],
                ),
                test_type="brow",
                test_name=test["name"],
            )

    def test_next_extraction(self) -> None:
        for test in self.test_next:
            self._do_extraction_test(
                func=lambda: self.innertube.next(
                    video_id=test["video_id"],
                    playlist_id=test["playlist_id"],
                    params=test["params"],
                    index=test["index"],
                    continuation=test["continuation"],
                ),
                test_type="next",
                test_name=test["name"],
            )

    def test_player_extraction(self) -> None:
        for test in self.test_next:
            self._do_extraction_test(
                func=lambda: self.innertube.player(
                    video_id=test["video_id"]
                ),
                test_type="play",
                test_name=test["name"],
            )

    def test_serialization(self) -> None:
        for name, container in self.ext_containers.items():
            if container is not None:
                try:
                    dump = container.dump()
                    self.ser_containers[name] = dump

                    if self.save_data:
                        with open(os.path.join(self.dump_path, f"{name}.json"), mode="w") as file:
                            json.dump(dump, file, indent=4)
                    self.ser_log.append(f"{name} [green][OK][/green]")

                except Exception:
                    log.exception(f"{name}: serialization error")
                    self.ser_log.append(f"{name} [red][ER][/red]")
                    self.ser_containers[name] = None

            else:
                self.ser_containers[name] = None
                self.ser_log.append(f"{name} [yellow][NE][/yellow]")

    def test_deserialization(self) -> None:
        for name, container_data in self.ser_containers.items():
            if container_data is not None:

                container = Container()

                try:
                    container.load(container_data)  

                except Exception:
                    log.exception(f"{name}: deserialization error")
                    self.des_log.append(f"{name} [red][ER][/red]")
                    self.des_containers[name] = None

                else:
                    self.des_containers[name] = container
                    self.des_log.append(f"{name} [green][OK][/green]")

            else:
                self.des_log.append(f"{name} [yellow][NE][/yellow]")
                self.des_containers[name] = None

    def test_data_integrity(self) -> None:
        for name, container in self.des_containers.items():
            
            if container is None:
                self.dat_log.append(f"{name} [yellow][NE][/yellow]")

            else:
                try:
                    compare_container(container, self.ext_containers[name])
                    check_container(container)                  # type: ignore
                    check_container(self.ext_containers[name])  # type: ignore
                        
                    if self.ext_containers[name] == container:
                        self.dat_log.append(f"{name} [green][OK][/green]")
                    else:
                        self.dat_log.append(f"{name} [red][ER][/red]")

                except AssertionError:
                    log.exception(f"{name}: data integrity error")
                    self.dat_log.append(f"{name} [red][ER][/red]")

    def _do_extraction_test(self, func: Callable, test_type: str, test_name: str) -> None:
        name = f"{test_type}_{test_name}"
        cs.print()
        cs.print(f"[blue]{name}[/blue]")
        try:
            innertube_data = get_innertube_data(func)
            ext_container = self.extractor.extract(innertube_data)

        except (RequestError, ConnectError):
            log.exception(f"{name}: innertube error")
            self.ext_log.append(f"{name} [yellow][NE][/yellow]")
            self.ext_containers[name] = None

        except ExtractionError:
            log.exception(f"{name}: extraction error")
            self.ext_log.append(f"{name} [red][ER][/red]")
            self.ext_containers[name] = None

            if self.save_data is True:
                with open(os.path.join(self.errs_path, f"{name}.json"), mode="w") as file:
                    json.dump(innertube_data, file, indent=4)  # noqa # type: ignore

        except Exception:
            log.exception("tester error")

        else:
            self.ext_log.append(f"{name} [green][OK][/green]")
            self.ext_containers[name] = ext_container
            if self.verbose:
                print_container(ext_container)
            if self.save_data:
                with open(os.path.join(self.inne_path, f"{name}.json"), mode="w") as file:
                    json.dump(innertube_data, file, indent=4)


def print_logs(
        testers: List[Tester], 
        distance: int = 0, 
        *,
        center: bool = True, 
        vertical_view: bool = False
) -> None:
    if len(testers) == 0:
        return

    def rstring(string: str) -> str:
        return (" " * distance).join([string for _ in range(len(testers))])

    def get_table_line(tester: Tester, index: int) -> str:
        table_line = f"| {tester.ext_log[index]} "
        table_line += f"| {tester.ser_log[index]} "
        table_line += f"| {tester.des_log[index]} "
        table_line += f"| {tester.dat_log[index]} |"
        return table_line

    LENGTH = 77
    def get_table_name(tester: Tester) -> str:
        ns = 0 if center is False else LENGTH // 2 - len(tester.target.value) // 2
        sxs = " " * (LENGTH + distance - len(tester.target.value) - ns)
        return f"{' ' * ns}{tester.target.value.upper()}{sxs}"

    table_horizontal = "+------------------" * 4 + "+"
    ext_col = "| [blue]EXTRACTION[/blue]       "
    ser_col = "| [blue]SERIALIZATION[/blue]    "
    des_col = "| [blue]DESERIALIZATION[/blue]  "
    dat_col = "| [blue]DATA INTEGRITY[/blue]   |"
    table_header = f"{ext_col}{ser_col}{des_col}{dat_col}"

    td = get_terminal_dimensions()
    max_width = len(testers) * LENGTH + (distance * len(testers))
    vertical_view = (td[1] < max_width or vertical_view) if td is not None else True

    cs.print()
    if vertical_view:
        for tester in testers:
            cs.print(f"[blue]{get_table_name(tester)}[/blue]")
            cs.print(table_horizontal)
            cs.print(table_header)
            for i in range(len(tester.ext_log)):
                cs.print(get_table_line(tester,  i))
            cs.print(table_horizontal)
            cs.print()
    else:
        table_names = ""
        closed: Dict[Tester, bool] = {}
        for i, tester in enumerate(testers):
            table_names += get_table_name(tester)
            closed[tester] = False

        cs.print(f"[blue]{table_names}[/blue]")
        cs.print(rstring(table_horizontal))
        cs.print(rstring(table_header))
        for i in range(max(map(len, [tester.ext_log for tester in testers])) + 1):
            table_line = ""
            for j, tester in enumerate(testers):
                if i >= len(tester.ext_log):
                    if closed[tester] is False:
                        table_line += f"{' ' * distance if j > 0 else ''}{table_horizontal}"
                        closed[tester] = True
                    else:
                        table_line += " " * LENGTH
                else:
                    if j > 0:
                        table_line += " " * distance
                    table_line += get_table_line(tester, i)
            cs.print(table_line)


def print_container(container: Container) -> None:
    if container.contents is None:
        return
    for shelf in container.contents:
        shelf_type = "CardShelf" if isinstance(shelf, CardShelf) else "Shelf"
        cs.print()
        cs.print(f"{shelf_type} Name: {shelf.name}")
        cs.print(f"{shelf_type} Endpoint: {shelf.endpoint}")
        if isinstance(shelf, CardShelf):
            cs.print(f"{shelf_type} Item: {shelf.item}")
        cs.print(f"{shelf_type} Items: ", end="")
        if len(shelf) != 0:
            cs.print("\n", end="")
            for item in shelf:
                cs.print(f"{str(item)}")
        else:
            cs.print("None")


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_false')
    parser.add_argument('--save-data', '-s', action='store_false')
    parser.add_argument('--enable-exceptions', '-ee', action='store_false')
    parser.add_argument('--log-errors', '-le', action='store_false')
    parser.add_argument('--stack-info', '-si', action='store_false')
    parser.add_argument('--exc-info', '-ei', action='store_false')
    parser.add_argument('--include-all-urls', '-iau', action='store_false')
    parser.add_argument('--youtube-music', '-ym', action='store_false')
    parser.add_argument('--youtube', '-yt', action='store_false')
    parser.add_argument('--vertical-mode', '-vm', action='store_true')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    targets: List[Tuple[paths.Target, str]] = []
    if args.youtube_music is True:
        targets.append((paths.Target.YOUTUBE_MUSIC, "WEB_REMIX"))
    if args.youtube is True:
        targets.append((paths.Target.YOUTUBE, "WEB"))

    testers: List[Tester] = []
    for target, client in targets:
        tester = Tester(
            target=target,
            innertube=InnerTube(client),
            verbose=args.verbose,
            save_data=args.save_data,

            # InnerTubeDE
            log_errors=args.log_errors,
            stack_info=args.stack_info,
            exc_info=args.exc_info,
            enable_exceptions=args.enable_exceptions,
            include_all_urls=args.include_all_urls
        )

        testers.append(tester)

    for tester in testers:
        tester.test_search_extraction()
        tester.test_browse_extraction()
        tester.test_next_extraction()
        # tester.test_player_extraction()

        tester.test_serialization()
        tester.test_deserialization()
        tester.test_data_integrity()

    print_logs(
        testers, 
        distance=10, 
        center=True, 
        vertical_view=args.vertical_mode
    )


if __name__ == "__main__":
    main()

