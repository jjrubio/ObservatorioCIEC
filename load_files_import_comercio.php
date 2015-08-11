<?php
$servername = 'localhost';
$username = 'root';
$password = 'root';
$dbname = 'OESE';
$conn = mysqli_connect($servername, $username, $password, $dbname);
if ($conn->connect_error){
    die ('Conexion fallida: '.$conn->connect_error);
}
include '/home/patu/Downloads/ObservatorioCIEC-master/static/Classes/PHPExcel/IOFactory.php';
foreach (glob("/home/patu/Downloads/ObservatorioCIEC-master/media/csv/*") as $inputFileName){
    //  Read your Excel workbook
    try {
        $inputFileType = PHPExcel_IOFactory::identify($inputFileName);
        $objReader = PHPExcel_IOFactory::createReader($inputFileType);
        $objPHPExcel = $objReader->load($inputFileName);
    } catch(Exception $e) {
        die('Error loading file "'.pathinfo($inputFileName,PATHINFO_BASENAME).'": '.$e->getMessage());
    }    
    foreach ($objPHPExcel->getWorksheetIterator() as $worksheet) {
        foreach ($worksheet->getRowIterator() as $row) {
            $cellIterator = $row->getCellIterator();
            $cellIterator->setIterateOnlyExistingCells(false);
        $i = 0;
            $y = 0;
            $array = array();
            $array_int = array();
            foreach ($cellIterator as $cell) {
                if ($cell->getValue() == 'YEAR' or $cell->getValue() == 'MES' or $cell->getValue() == 'PAIS' or $cell->getValue() == 'SUBPARTIDA NANDINA' or $cell->getValue() == 'DESCRIPCION NANDINA' or $cell->getValue() == 'PESO - KILOS' or $cell->getValue() == 'FOB - DOLAR' or $cell->getValue() == 'CIF - DOLAR' or $cell->getValue() == '% / TOTAL FOB - DOLAR'){
                    continue;
                }else{
                    $array[$i] = $cell->getValue();
                    $i++;
                }
            } 
            //Inserto los datos y borro los arreglos $array
        if (!empty($array[0])) {
                $ano_int = intval($array[0]);
                $mes_int = intval($array[1]);
                $pais_int = intval($array[2]);
                $subpartida_nandina_int = intval($array[3]);
                $peso_float = floatval($array[5]);
                $fob_float = floatval($array[6]);
                $cif_float = floatval($array[7]);
                $sql = "INSERT INTO comercio_import_nandina".
               "(ano,mes,pais,subpartida_nandina,peso,fob,cif)".
               "VALUES ".
               "($ano_int,$mes_int,$pais_int,$subpartida_nandina_int,$peso_float,$fob_float,$cif_float);";
        if (mysqli_query($conn, $sql)) {
                    echo "New record created successfully";
                } else {
                    echo "Error: " . $sql . "<br>" . mysqli_error($conn);
                }
            }
            unset($array);
            unset($array_int);
        }
    }
}
mysqli_close($conn);
?>