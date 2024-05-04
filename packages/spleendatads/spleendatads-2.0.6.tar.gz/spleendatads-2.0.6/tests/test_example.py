from pathlib import Path

from spleendatads import parser, main


def test_main(tmp_path: Path, capsys):
    # setup example data
    inputdir = tmp_path / "incoming"
    outputdir = tmp_path / "outgoing"
    inputdir.mkdir()
    outputdir.mkdir()
    (inputdir / "plaintext.txt").write_text("hello ChRIS, I am a ChRIS plugin")

    # simulate run of main function
    options = parser.parse_args(["--man"])
    main(options, inputdir, outputdir)

    # assert behavior is expected
    captured = capsys.readouterr()
    assert "SYNOPSIS" in captured.out
