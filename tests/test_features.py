from fair_ssf_opt.features import optimization_category, parse_process_parameters, substrate_family


def test_parameter_parser_decimal_comma():
    result = parse_process_parameters("pH=5,5 ; MC=70% ; T°=28,5°C ; Agitation=125rpm")
    assert result["ph"] == 5.5
    assert result["moisture_content_pct"] == 70.0
    assert result["temperature_c"] == 28.5
    assert result["agitation_rpm"] == 125.0


def test_optimization_categories():
    assert optimization_category("RSM (Box-Behnken design)") == "RSM"
    assert optimization_category("OFAT") == "OFAT"
    assert optimization_category("Taguchi design") == "Taguchi"
    assert optimization_category("None") == "none"


def test_substrate_family():
    assert substrate_family("mixture (wheat bran ; sugarcane bagasse)") == "wheat"
    assert substrate_family("mixture (rice straw ; wheat bran)") == "rice+wheat"
