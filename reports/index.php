<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Backup Report List</title>
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="stylesheet" href="backup-report-stylesheet.css">
	<style>
		div.summary_line {
			border-top: 1px solid silver;
		}
		div.recent_reports_error {
			width: 100%;
			padding: 10px 0;
			background-color: red;
			text-align: center;
		}
	</style>
</head>
<body>
<div class="position">
	<div class="report">
		<h1>Backup Report List</h1>
		<div class="summary">
<?php

$today = time();
$yesterday = strtotime('-1 day');
$todays_reports = glob("backup_report_".strftime("%Y-%m-%d", $today)."*.html");
$yesterdays_reports = glob("backup_report_".strftime("%Y-%m-%d", $yesterday)."*.html");
$recent_reports = array_merge($todays_reports, $yesterdays_reports);
if (count($recent_reports) == 0) {
?>
	<div class="recent_reports_error">
		ERROR: There are no backup reports for today or yesterday!
	</div>
<?php
}

$report_list = glob("backup_report_*.html");
rsort($report_list);
$report_list = array_slice($report_list, 0, 100);
$script_name = "index.php";
if (substr($_SERVER[REQUEST_URI], -strlen($script_name)) == $script_name) {
	$link = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http") . "://".$_SERVER[HTTP_HOST].dirname($_SERVER[REQUEST_URI]);
}
else {
	$link = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http") . "://".$_SERVER[HTTP_HOST].$_SERVER[REQUEST_URI];
}
$previous_year = "";
$previous_month = "";
$needle = '<div class="summary_cell_result fail">';
foreach ($report_list as $report_file) {
	$report_name_array = explode("_", str_replace("-", "_", $report_file));
	$year = $report_name_array[2];
	$month = $report_name_array[3];
	$day = $report_name_array[4];
	$dayname = $report_name_array[5];
	$hour = $report_name_array[6];
	$minute = $report_name_array[7];
	if (($year != $previous_year) && ($month != $previous_month)) {
		$month_name = date('F', mktime(0, 0, 0, $month, 10));
		echo("<h2>".$month_name." ".$year."</h2>\n");
	}
	$previous_year = $year;
	$previous_month = $month;
?>

		<div class="summary_line">
			<div class="summary_cell_host">
				<a href="<?php echo($link.$report_file) ?>">
					<?php echo("$dayname. $day.$month.$year $hour:$minute"); ?>
				</a>
			</div>
			
<?php	
	$success = false;
	$handle = fopen("$report_file", "r");
	if ($handle) {
		$success = true;
		while (($line = fgets($handle)) !== false) {
			if (strpos($line, $needle) !== false) {
				$success = false;
				break;
			}
		}
		fclose($handle);
	}
	if ($success == true) {
		echo("<div class=\"summary_cell_result success\">SUCCESS</div>\n");
	}
	else {
		echo("<div class=\"summary_cell_result fail\">FAIL</div>\n");
	}
?>
		</div>

<?php	
}
?>
		</div>
	</div>
</div>
</body>
</html>