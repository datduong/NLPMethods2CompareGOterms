# This code finalizes (extended) definitions of GO terms included in MF ontology for their definition vectors (Please read the read-me file before use!)
use IO::File;

# "../../Extra/MF/MF_Pre_Definition_Matrix.dat"
# "../../Matrices/MF_Definition_Matrix.mtrx"
# "../../Extra/MF/MF_Pre_Definition_Matrix_temp.dat"

my ($nameInput,$preMatrixDefinition,$matrixDefinition) = @ARGV;

my $r1 = IO::File->new($nameInput,"r") or die "Can not open file to read from;\nRun '2.7.MF_Definition_Matrix_Construction_preparation.pl' first!\n";
my $r2 = IO::File->new("../../Extra/word_index.dat","r") or die  "Can not open file to read from;\nRun '1.1.Bigrams_2_Sparse_4_R_preparation.pl' first!\n";
open(my $w, '>', $preMatrixDefinition) or die "Could not open file to write in\n";

my $k = 1;
my $dim2;
%hash;
foreach(<$r2>){
	if($k == 1){$k++; next;}
	chomp;
	my @a = split " ";
	$hash{$a[0]} = $a[1];
	$dim2 = $a[1];
}

my $sum;
my $dim1 = 1;
foreach(<$r1>){
	chomp;
	my @a = split ":: ";
	my @b = split " ", $a[1];
	
	my $j = 0;
	while(defined $b[$j]){
		$w->print("$dim1 $hash{$b[$j]} $b[$j+1]\n");
		$sum += $b[$j+1];
		$j+=2;
	}
	$dim1++;
}

close $w;

my $r3 = IO::File->new($preMatrixDefinition,"r") or die "Could not open file to read from\n";
open(my $w1, '>', $matrixDefinition) or die "Could not open file to write in\n";

$dim1 = $dim1 - 1;
$w1->print("%%MatrixMarket matrix coordinate real general\n"); ### This line is only for R (For MATLAB usage comment this out)
$w1->print("$dim1 $dim2 $sum\n");

while(<$r3>){
	$w1->print($_);
}
